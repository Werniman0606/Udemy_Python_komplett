# ==============================================================================
# Dateiname: dateiname_aus_digikam_tags_rekonstruieren.py
# Beschreibung: Liest XMP-Metadaten (Personennamen) mit ExifTool und konstruiert
#               daraus das [Tag1, Tag2]_ Präfix für den Dateinamen.
#
# Statusanzeige-Update: Zeigt den alten und den neuen Dateinamen bei jeder
#                       erfolgreichen Umbenennung klar an.
# ==============================================================================

import os
import subprocess
import json
import codecs
import re  # Füge re für die find_existing_prefix Korrektur hinzu

# Konfigurieren des zu durchsuchenden Ordners
ROOT_FOLDER = r"e:\Bilder\Celebrities\D\Donna Edmondson"

# EXIFTOOL PFAD ANPASSUNG
EXIFTOOL_PATH = r"d:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe"


def get_persons_from_file(filepath):
    """
    Ruft ExifTool auf, um die TagsList zu lesen und extrahiert die Personennamen.
    Entfernt doppelte Namen.
    """
    persons = []
    # Verwende '-TagsList' um die Digikam-Hierarchie (z.B. Personen/Max) zu erhalten.
    cmd = [EXIFTOOL_PATH, '-TagsList', '-j', filepath]

    try:
        # Verwende das 'ignore'-Verhalten für Fehler beim Dekodieren
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        if not result.stdout.strip():
            return persons

        # ExifTool gibt ein JSON-Array zurück, auch bei einer Datei
        output_json = json.loads(result.stdout)

        if output_json and output_json[0] and 'TagsList' in output_json[0]:
            digikam_tags = output_json[0]['TagsList']

            # Stelle sicher, dass digikam_tags als Liste behandelt wird
            tags_to_process = digikam_tags if isinstance(digikam_tags, list) else [digikam_tags]

            for tag in tags_to_process:
                # Prüfe nur Tags, die mit der Digikam-Kategorie 'Personen/' beginnen
                if isinstance(tag, str) and tag.startswith("Personen/"):
                    # Füge den reinen Namen ohne das Präfix 'Personen/' hinzu
                    persons.append(tag.split("/", 1)[1].strip())

    except subprocess.CalledProcessError as e:
        print(f"FEHLER bei ExifTool-Ausführung für '{filepath}': {e.stderr}")
    except json.JSONDecodeError:
        print(f"FEHLER: Ungültiges JSON von ExifTool für '{filepath}' erhalten.")
    except Exception as e:
        print(f"FEHLER beim Verarbeiten der ExifTool-Ausgabe für '{filepath}': {e}")

    # Duplikate entfernen und alphabetisch sortieren
    return sorted(list(set(persons)))


def create_prefix(persons, safe_mode=False):
    """
    Erstellt den Dateinamen-Präfix. Die Personen sind bereits sortiert.
    Wenn safe_mode=True, werden Umlaute ersetzt (Stufe 1: AE/OE/UE).
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
                # Ersetzung muss Groß- und Kleinschreibung berücksichtigen
                current_name = current_name.replace(old, new)
        processed_persons.append(current_name)

    # Die Personen sind bereits sortiert, nur noch zusammenfügen
    return f"[{', '.join(processed_persons)}]_"


def find_existing_prefix(filename):
    """
    Prüft, ob der Dateiname mit einem Präfix in eckigen Klammern beginnt und gibt diesen zurück.
    """
    # Regex sucht nach: Start, [, beliebige Zeichen (nicht \) ], _, beliebige Zeichen
    match = re.match(r'^\[.*?\]_', filename)
    if match:
        # Gibt den gesamten Präfix zurück, z.B. "[Max Mustermann]_"
        return match.group(0)
    return None


def rename_file_with_persons(filepath, persons):
    """
    Benennt die Datei in zwei Schritten um: erst mit Ersatzzeichen (Safe), dann mit korrekten Umlauten (Final).
    """
    if not persons:
        # Nur umbenennen, wenn Personen-Tags gefunden wurden
        return False

    original_dirname = os.path.dirname(filepath)
    original_basename = os.path.basename(filepath)
    filename_without_ext, ext = os.path.splitext(original_basename)

    # Der aktuelle Pfad ist der Pfad vor JEDER Umbenennung
    current_filepath = filepath

    # --- 1. Generierung der Präfix-Varianten ---
    safe_prefix = create_prefix(persons, safe_mode=True)
    final_prefix = create_prefix(persons, safe_mode=False)

    # --- 2. Bestimmung des Basisnamens (ohne alten Präfix) ---
    base_name_without_prefix = filename_without_ext
    existing_prefix = find_existing_prefix(original_basename)

    if existing_prefix:
        # Schneide den erkannten, alten Präfix vom Namen ohne Endung ab
        base_name_without_prefix = filename_without_ext[len(existing_prefix):]

    # --- 3. Neuberechnung der vollständigen neuen Pfade ---
    new_basename_safe = f"{safe_prefix}{base_name_without_prefix}{ext}"
    new_filepath_safe = os.path.join(original_dirname, new_basename_safe)

    new_basename_final = f"{final_prefix}{base_name_without_prefix}{ext}"
    new_filepath_final = os.path.join(original_dirname, new_basename_final)

    # Wenn der Name bereits dem finalen Schema entspricht, nichts tun
    if original_basename == new_basename_final:
        return False

    # --- 4. Ausführung der Umbenennungslogik ---

    # --- Fall A: Umbenennung von Stufe 1 (Safe) auf Stufe 2 (Final) ---
    # Dies geschieht, wenn die Datei bereits einmal verarbeitet wurde, aber der finale Schritt mit Umlauten noch fehlt.
    if existing_prefix == safe_prefix:
        if safe_prefix == final_prefix:
            return False  # Keine Umlaute, Stufe 1 ist bereits Stufe 2

        try:
            if os.path.exists(new_filepath_final):
                print(f"WARNUNG: Finaler Name '{new_basename_final}' existiert bereits.")
                return False

            os.rename(current_filepath, new_filepath_final)
            print(f"    ✅ UMBENANNT (Stufe 1 -> Stufe 2): '{original_basename}' -> **{new_basename_final}**")
            return True
        except Exception as e:
            print(f"FEHLER beim Umbenennen (Stufe 1 -> Stufe 2) von '{original_basename}': {e}")
            return False

    # --- Fall B: Erstmalige oder allgemeine Umbenennung (Original/Alt -> Safe/Stufe 1) ---

    try:
        # SCHRITT 1: Original oder Alter Präfix -> Safe (mit ae/oe/ue)
        # Stelle sicher, dass wir nicht unnötig von Original auf Original umbenennen
        if original_basename != new_basename_safe:
            os.rename(current_filepath, new_filepath_safe)
            print(f"    ✅ UMBENANNT (Original/Alt -> Stufe 1): '{original_basename}' -> **{new_basename_safe}**")
            # Setze den aktuellen Pfad für den nächsten Schritt
            current_filepath = new_filepath_safe
        else:
            # Wenn Originalname = Safe-Name, kein Umbenennen auf Stufe 1
            pass

        # SCHRITT 2: Safe -> Final (mit ä/ö/ü) - nur wenn Umlaute vorhanden sind (safe != final)
        if safe_prefix != final_prefix:

            if os.path.exists(new_filepath_final):
                print(
                    f"WARNUNG: Finaler Dateiname '{new_basename_final}' existiert bereits. "
                    f"Lösche temporäre Safe-Datei '{os.path.basename(current_filepath)}'.")
                # Lösche die temporäre Safe-Datei, da die finale Version schon da ist
                os.remove(current_filepath)
                return True

            os.rename(current_filepath, new_filepath_final)
            print(
                f"    ✅ UMBENANNT (Stufe 1 -> Stufe 2): '{os.path.basename(current_filepath)}' -> **{new_basename_final}**")
            return True

        return True  # Umbenennung zu Stufe 1 ist der finale Zustand (keine Umlaute)

    except FileExistsError:
        print(
            f"WARNUNG: Umbenennung von '{original_basename}' fehlgeschlagen, da '{new_basename_safe}' bereits existiert.")
        return False
    except Exception as e:
        print(f"FEHLER beim Umbenennen von '{original_basename}': {e}")
        return False


def main():
    """
    Hauptfunktion, die den Ordner durchläuft und Dateien verarbeitet.
    """
    if not os.path.isdir(ROOT_FOLDER):
        print(f"Fehler: Der angegebene Ordner '{ROOT_FOLDER}' existiert nicht.")
        return

    if not os.path.isfile(EXIFTOOL_PATH):
        print(f"Fehler: Die Datei '{EXIFTOOL_PATH}' wurde nicht gefunden.")
        print("Bitte überprüfen Sie den Pfad zu exiftool.exe im Skript.")
        return

    print(f"Starte die Umbenennung in '{ROOT_FOLDER}'...")
    print("--------------------------------------------------------------------------------")
    renamed_count = 0

    for dirpath, _, filenames in os.walk(ROOT_FOLDER):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                continue

            # Liest immer die aktuellen Metadaten, um den erforderlichen Namenspräfix zu bestimmen
            persons = get_persons_from_file(filepath)

            if persons:
                print(f"\n[PRÜFE] Aktuelle Datei: {filename}")
                print(f"    Tags gefunden: {', '.join(persons)}")

                if rename_file_with_persons(filepath, persons):
                    renamed_count += 1
            # else: Datei ohne Personen-Tags wird ignoriert.

    print("--------------------------------------------------------------------------------")
    print("Verarbeitung abgeschlossen.")
    print(f"Insgesamt wurden {renamed_count} Dateien umbenannt/aktualisiert.")
    print("--------------------------------------------------------------------------------")


if __name__ == "__main__":
    main()