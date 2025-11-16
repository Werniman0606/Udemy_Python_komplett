# ==============================================================================
# Dateiname Vorschlag (Deutsch): exif_prefix_umbenennung_zwei_stufen.py
# Dateiname Vorschlag (Technisch): exiftool_tag_to_filename_two_stage.py
#
# Beschreibung: Dieses Skript liest die in den XMP-Metadaten (speziell
#               TagsList/Personen-Tags) gespeicherten Personennamen aus
#               Bilddateien. Es generiert daraus einen Präfix im Format
#               "[Name1, Name2]_" und benennt die Datei in einem
#               Zwei-Stufen-Prozess um (erst mit Umlaut-Ersatz, dann mit
#               korrekten Umlauten), um Kompatibilitätsprobleme zu umgehen.
#               Die Umbenennung wird nur durchgeführt, wenn der aktuelle Name
#               nicht dem erforderlichen Zielnamen entspricht.
# ==============================================================================

import os
import subprocess
import json
import codecs
import re

# Konfigurieren des zu durchsuchenden Ordners
ROOT_FOLDER = r"d:\RedditDownloads\reddit_sub_GermanCelebs"

# EXIFTOOL PFAD ANPASSUNG
EXIFTOOL_PATH = r"d:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe"


def get_persons_from_file(filepath):
    """
    Ruft ExifTool auf, um die TagsList zu lesen (im JSON-Format) und extrahiert
    die Personennamen, die mit "Personen/" beginnen. Entfernt doppelte Namen.
    """
    persons = []
    # -j gibt die Ausgabe als JSON, -TagsList liest das Tag
    cmd = [EXIFTOOL_PATH, '-TagsList', '-j', filepath]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        if not result.stdout.strip():
            return persons

        output_json = json.loads(result.stdout)

        if output_json and output_json[0] and 'TagsList' in output_json[0]:
            digikam_tags = output_json[0]['TagsList']

            # TagsList kann eine Liste oder ein einzelner String sein
            if isinstance(digikam_tags, list):
                for tag in digikam_tags:
                    if tag.startswith("Personen/"):
                        persons.append(tag.split("/", 1)[1])
            elif isinstance(digikam_tags, str) and digikam_tags.startswith("Personen/"):
                persons.append(digikam_tags.split("/", 1)[1])

    except subprocess.CalledProcessError as e:
        print(f"Fehler bei ExifTool-Ausführung für '{filepath}': {e.stderr}")
    except json.JSONDecodeError:
        print(f"Fehler: Ungültiges JSON von ExifTool für '{filepath}' erhalten.")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der ExifTool-Ausgabe für '{filepath}': {e}")

    # Duplikate entfernen und in eine Liste zurückwandeln
    return list(set(persons))


def create_prefix(persons, safe_mode=False):
    """
    Erstellt den Dateinamen-Präfix. Die Personen werden alphabetisch sortiert.
    Wenn safe_mode=True, werden Umlaute ersetzt (ä -> ae, etc.) für die Stufe 1.
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

    # Sortierung der Namen im Präfix
    sorted_persons = sorted(processed_persons)

    return f"[{', '.join(sorted_persons)}]_"


def find_existing_prefix(filename):
    """
    Prüft, ob der Dateiname mit einem Präfix in eckigen Klammern beginnt und gibt diesen zurück.
    Der Präfix muss mit '_]' enden, um gültig zu sein.
    """
    if filename.startswith('['):
        try:
            # Finde das schließende eckige Klammer-Zeichen und den Unterstrich
            end_index = filename.index(']_')
            # Gibt den gesamten Präfix zurück, z.B. "[Max Mustermann]_"
            return filename[:end_index + 2]
        except ValueError:
            # Kein '_]' gefunden, also kein gültiger Präfix
            return None
    return None


def rename_file_with_persons(filepath, persons):
    """
    Benennt die Datei in zwei Schritten um: erst mit Ersatzzeichen (Safe), dann mit korrekten Umlauten (Final).
    Diese zweistufige Logik dient zur Vermeidung von Problemen bei der Umbenennung von Umlaut-Namen.
    """
    if not persons:
        return False

    original_dirname = os.path.dirname(filepath)
    original_basename = os.path.basename(filepath)
    filename_without_ext, ext = os.path.splitext(original_basename)

    # --- 1. Generierung der Präfix-Varianten ---
    safe_prefix = create_prefix(persons, safe_mode=True)
    final_prefix = create_prefix(persons, safe_mode=False)

    # --- 2. Bestimmung des Basisnamens (ohne alten Präfix) ---
    base_name = filename_without_ext

    existing_prefix = find_existing_prefix(original_basename)
    if existing_prefix:
        # Schneide den erkannten, alten Präfix vom Namen ohne Endung ab
        base_name = filename_without_ext[len(existing_prefix):]

    # --- 3. Neuberechnung der vollständigen neuen Pfade ---

    new_basename_safe = f"{safe_prefix}{base_name}{ext}"
    new_filepath_safe = os.path.join(original_dirname, new_basename_safe)

    new_basename_final = f"{final_prefix}{base_name}{ext}"
    new_filepath_final = os.path.join(original_dirname, new_basename_final)

    # Prüfen, ob der Dateiname bereits dem finalen, korrekten Schema entspricht
    if original_basename == new_basename_final:
        return False # Bereits korrekt benannt.

    # --- 4. Ausführung der Umbenennungslogik ---

    # Fall A: Originalname beginnt mit Safe-Präfix (Datei ist auf Stufe 1, muss auf Stufe 2)
    if existing_prefix and existing_prefix == safe_prefix:
        if safe_prefix == final_prefix:
            return False # Keine Umlaute, Stufe 1 ist bereits Stufe 2

        try:
            if os.path.exists(new_filepath_final):
                print(f"WARNUNG: Finaler Name '{new_basename_final}' existiert bereits.")
                return False

            os.rename(filepath, new_filepath_final)
            print(f"Aktualisiert (Stufe 1 -> Stufe 2): '{original_basename}' -> '{new_basename_final}'")
            return True
        except Exception as e:
            print(f"FEHLER beim Umbenennen (Stufe 1 -> Stufe 2) von '{original_basename}': {e}")
            return False

    # Fall B: Allgemeine Umbenennung (Original/Aktualisierung -> Safe -> Final).
    try:
        # SCHRITT 1: Original oder Alter Präfix -> Safe (mit ae/oe/ue)
        os.rename(filepath, new_filepath_safe)
        print(f"Umbenannt (Original/Aktualisiert -> Stufe 1): '{original_basename}' -> '{new_basename_safe}'")

        # SCHRITT 2: Safe -> Final (mit ä/ö/ü) - nur wenn Umlaute vorhanden sind
        if safe_prefix != final_prefix:

            if os.path.exists(new_filepath_final):
                print(
                    f"WARNUNG: Finaler Dateiname '{new_basename_final}' existiert bereits. "
                    f"Überspringe finale Umbenennung und lösche temporäre Safe-Datei.")
                os.remove(new_filepath_safe)
                return True

            os.rename(new_filepath_safe, new_filepath_final)
            print(f"Umbenannt (Stufe 1 -> Stufe 2): '{new_basename_safe}' -> '{new_basename_final}'")
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
    Hauptfunktion, die den Ordner rekursiv durchläuft und Dateien verarbeitet.
    """
    if not os.path.isdir(ROOT_FOLDER):
        print(f"Fehler: Der angegebene Ordner '{ROOT_FOLDER}' existiert nicht.")
        return

    if not os.path.isfile(EXIFTOOL_PATH):
        print(f"Fehler: Die Datei '{EXIFTOOL_PATH}' wurde nicht gefunden.")
        print("Bitte überprüfen Sie den Pfad zu exiftool.exe im Skript.")
        return

    print(f"Starte die Umbenennung in '{ROOT_FOLDER}'...")
    renamed_count = 0

    for dirpath, _, filenames in os.walk(ROOT_FOLDER):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                continue

            # Liest die aktuellen Metadaten, um den erforderlichen Namenspräfix zu bestimmen
            persons = get_persons_from_file(filepath)

            if rename_file_with_persons(filepath, persons):
                renamed_count += 1

    print("-" * 50)
    print("Verarbeitung abgeschlossen.")
    print(f"Insgesamt wurden {renamed_count} Dateien umbenannt.")
    print("-" * 50)


if __name__ == "__main__":
    main()