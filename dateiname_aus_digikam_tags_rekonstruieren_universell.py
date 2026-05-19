# ==============================================================================
# Dateiname: dateiname_aus_digikam_tags_rekonstruieren.py
# Beschreibung: Liest XMP-Metadaten (Personennamen) mit ExifTool und konstruiert
#                daraus das [Tag1, Tag2]_ Präfix für den Dateinamen.
#
# Funktioniert nativ unter Windows UND Linux (CachyOS).
# ==============================================================================

import os
import subprocess
import json
import re
from pathlib import Path

# --- KONFIGURATION & BETRIEBSSYSTEM-ERKENNUNG ---
if os.name == 'nt':  # Windows
    ROOT_FOLDER = Path(r"d:\extracted\rips")
    EXIFTOOL_PATH = Path(r'D:\exiftool-13.52_64\exiftool-13.52_64\exiftool.exe')
else:  # Linux (CachyOS)
    ROOT_FOLDER = Path("/run/media/marcoj/Laufwerk D/extracted/rips")
    EXIFTOOL_PATH = Path("/usr/bin/exiftool")
    # Falls es dort nicht liegt, Standardfall für den globalen Aufruf:
    if not EXIFTOOL_PATH.exists():
        EXIFTOOL_PATH = Path("exiftool")


def get_persons_from_file(filepath):
    """
    Ruft ExifTool auf, um die TagsList zu lesen und extrahiert die Personennamen.
    """
    persons = []
    # subprocess akzeptiert Path-Objekte, wenn sie in Strings konvertiert werden
    cmd = [str(EXIFTOOL_PATH), '-TagsList', '-j', str(filepath)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')

        if not result.stdout.strip():
            return persons

        output_json = json.loads(result.stdout)

        if output_json and len(output_json) > 0 and 'TagsList' in output_json[0]:
            digikam_tags = output_json[0]['TagsList']

            if isinstance(digikam_tags, str):
                tags_to_process = [digikam_tags]
            elif isinstance(digikam_tags, list):
                tags_to_process = digikam_tags
            else:
                tags_to_process = []

            for tag in tags_to_process:
                if isinstance(tag, str) and tag.startswith("Personen/"):
                    name = tag.split("/", 1)[1].strip()
                    persons.append(name)

    except Exception as e:
        print(f"FEHLER beim Verarbeiten von '{filepath.name}': {e}")

    return sorted(list(set(persons)))


def create_prefix(persons, safe_mode=False):
    """
    Erstellt den Dateinamen-Präfix. Die Personen sind bereits sortiert.
    """
    replacements = {
        'ä': 'ae', 'Ä': 'Ae',
        'ö': 'oe', 'Ö': 'Oe',
        'ü': 'ue', 'Ü': 'Ue',
        'ß': 'ss',
    }

    processed_persons = []
    for p in persons:
        current_name = p
        if safe_mode:
            for old, new in replacements.items():
                current_name = current_name.replace(old, new)
        processed_persons.append(current_name)

    return f"[{', '.join(processed_persons)}]_"


def find_existing_prefix(filename):
    """
    Prüft, ob der Dateiname mit einem Präfix in eckigen Klammern beginnt.
    """
    match = re.match(r'^\[.*?\]_', filename)
    if match:
        return match.group(0)
    return None


def rename_file_with_persons(filepath, persons):
    """
    Benennt die Datei um, indem der aktuelle Präfix basierend auf den gefundenen
    Tags (oder deren Fehlen) aktualisiert wird.
    """
    original_dirname = filepath.parent
    original_basename = filepath.name
    filename_without_ext = filepath.stem
    ext = filepath.suffix
    existing_prefix = find_existing_prefix(original_basename)

    # --- 1. Personen-Tags gefunden (Normaler Ablauf) ---
    if persons:
        safe_prefix = create_prefix(persons, safe_mode=True)
        final_prefix = create_prefix(persons, safe_mode=False)

        base_name_without_prefix = filename_without_ext
        if existing_prefix:
            base_name_without_prefix = filename_without_ext[len(existing_prefix):]

        new_basename_safe = f"{safe_prefix}{base_name_without_prefix}{ext}"
        new_filepath_final = original_dirname / f"{final_prefix}{base_name_without_prefix}{ext}"

        if original_basename == new_filepath_final.name:
            return False

        # Fall A: Umbenennung von Stufe 1 (Safe) auf Stufe 2 (Final)
        if existing_prefix == safe_prefix:
            if safe_prefix == final_prefix:
                return False

            try:
                if new_filepath_final.exists():
                    print(f"WARNUNG: Finaler Name '{new_filepath_final.name}' existiert bereits.")
                    return False

                filepath.rename(new_filepath_final)
                print(f"    ✅ UMBENANNT (Stufe 1 -> Stufe 2): '{original_basename}' -> **{new_filepath_final.name}**")
                return True
            except Exception as e:
                print(f"FEHLER beim Umbenennen (Stufe 1 -> Stufe 2) von '{original_basename}': {e}")
                return False

        # Fall B: Erstmalige oder allgemeine Umbenennung
        try:
            current_filepath = filepath
            if original_basename != new_basename_safe:
                new_filepath_safe = original_dirname / new_basename_safe
                current_filepath.rename(new_filepath_safe)
                print(f"    ✅ UMBENANNT (Original/Alt -> Stufe 1): '{original_basename}' -> **{new_basename_safe}**")
                current_filepath = new_filepath_safe

            if safe_prefix != final_prefix:
                if new_filepath_final.exists():
                    print(f"WARNUNG: Finaler Dateiname '{new_filepath_final.name}' existiert bereits. "
                          f"Lösche temporäre Safe-Datei '{current_filepath.name}'.")
                    current_filepath.unlink()  # pathlib-Ersatz für os.remove()
                    return True

                current_filepath.rename(new_filepath_final)
                print(
                    f"    ✅ UMBENANNT (Stufe 1 -> Stufe 2): '{current_filepath.name}' -> **{new_filepath_final.name}**")
                return True

            return True

        except FileExistsError:
            print(
                f"WARNUNG: Umbenennung von '{original_basename}' fehlgeschlagen, da '{new_basename_safe}' bereits existiert.")
            return False
        except Exception as e:
            print(f"FEHLER beim Umbenennen von '{original_basename}': {e}")
            return False

    # --- 2. KEINE Personen-Tags gefunden (Präfix entfernen) ---
    else:
        if existing_prefix:
            base_name_without_prefix = filename_without_ext[len(existing_prefix):]
            new_basename_clean = f"{base_name_without_prefix}{ext}"
            new_filepath_clean = original_dirname / new_basename_clean

            try:
                if original_basename == new_basename_clean:
                    return False

                filepath.rename(new_filepath_clean)
                print(f"    ⚠️ UMBENANNT (Präfix entfernt): '{original_basename}' -> **{new_basename_clean}**")
                return True
            except Exception as e:
                print(f"FEHLER beim Entfernen des Präfixes von '{original_basename}': {e}")
                return False

        return False


def main():
    """
    Hauptfunktion, die den Ordner durchläuft und Dateien verarbeitet.
    """
    if not ROOT_FOLDER.is_dir():
        print(f"Fehler: Der angegebene Ordner '{ROOT_FOLDER}' existiert nicht.")
        return

    # Überprüfe den ExifTool-Pfad nur, wenn er als absolute Datei angegeben ist
    if EXIFTOOL_PATH.is_absolute() and not EXIFTOOL_PATH.is_file():
        print(f"Fehler: ExifTool wurde unter '{EXIFTOOL_PATH}' nicht gefunden.")
        return

    print(f"Starte die Umbenennung in '{ROOT_FOLDER}'...")
    print("-" * 80)
    renamed_count = 0

    SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.webp')

    # rglob('*') durchsucht den Ordner rekursiv (wie os.walk)
    for file_path in ROOT_FOLDER.rglob('*'):
        # Nur Dateien verarbeiten, die eine unterstützte Endung haben
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:

            # Liest immer die aktuellen Metadaten
            persons = get_persons_from_file(file_path)
            existing_prefix = find_existing_prefix(file_path.name)

            if persons or existing_prefix:
                print(f"\n[PRÜFE] Aktuelle Datei: {file_path.name}")
                if persons:
                    print(f"    Tags gefunden: {', '.join(persons)}")
                else:
                    print("    Tags gefunden: KEINE")

                if rename_file_with_persons(file_path, persons):
                    renamed_count += 1

    print("-" * 80)
    print("Verarbeitung abgeschlossen.")
    print(f"Insgesamt wurden {renamed_count} Dateien umbenannt/aktualisiert.")
    print("-" * 80)


if __name__ == "__main__":
    main()