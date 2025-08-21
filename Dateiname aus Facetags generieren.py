import os
import subprocess
import json
import codecs

# Konfigurieren des zu durchsuchenden Ordners
ROOT_FOLDER = r"e:\Bilder"

# EXIFTOOL PFAD ANPASSUNG
EXIFTOOL_PATH = r"d:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe"


def get_persons_from_file(filepath):
    """
    Ruft ExifTool auf, um die TagsList zu lesen und extrahiert die Personennamen.
    """
    persons = []

    cmd = [
        EXIFTOOL_PATH,
        '-TagsList',
        '-j',
        filepath
    ]

    try:
        # Versucht primär, die Ausgabe als UTF-8 zu lesen
        # Bei einem Fehler werden die problematischen Zeichen ignoriert, um einen Abbruch zu verhindern
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')

        if not result.stdout.strip():
            return persons

        output_json = json.loads(result.stdout)

        if output_json and output_json[0] and 'TagsList' in output_json[0]:
            digikam_tags = output_json[0]['TagsList']

            if isinstance(digikam_tags, list):
                for tag in digikam_tags:
                    if tag.startswith("Personen/"):
                        person_name = tag.split("/", 1)[1]
                        persons.append(person_name)
            elif isinstance(digikam_tags, str):
                if digikam_tags.startswith("Personen/"):
                    person_name = digikam_tags.split("/", 1)[1]
                    persons.append(person_name)

    except subprocess.CalledProcessError as e:
        print(f"Fehler bei ExifTool-Ausführung für '{filepath}': {e.stderr}")
    except json.JSONDecodeError:
        print(f"Fehler: Ungültiges JSON von ExifTool für '{filepath}' erhalten.")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der ExifTool-Ausgabe für '{filepath}': {e}")

    return persons


def contains_umlaut(text):
    """
    Prüft, ob eine Zeichenkette Umlaute oder Sonderzeichen enthält.
    """
    return any(c in 'äöüÄÖÜß' for c in text)


def safe_name_from_persons(persons):
    """
    Erstellt einen sicheren Dateinamen-Präfix mit ersetzten Umlauten.
    """
    replacements = {
        'ä': 'ae', 'Ä': 'Ae',
        'ö': 'oe', 'Ö': 'Oe',
        'ü': 'ue', 'Ü': 'Ue',
        'ß': 'ss',
    }

    safe_persons = []
    for p in persons:
        for old, new in replacements.items():
            p = p.replace(old, new)
        safe_persons.append(p)

    sorted_persons = sorted(list(set(safe_persons)))
    return f"[{', '.join(sorted_persons)}]_"


def rename_file_with_persons(filepath, persons):
    """
    Benennt die Datei in zwei Schritten um: erst mit Ersatzzeichen, dann mit korrekten Umlauten.
    """
    if not persons:
        return False

    original_dirname = os.path.dirname(filepath)
    original_basename = os.path.basename(filepath)
    filename_without_ext, ext = os.path.splitext(original_basename)

    safe_prefix = safe_name_from_persons(persons)
    new_basename_safe = f"{safe_prefix}{filename_without_ext}{ext}"
    new_filepath_safe = os.path.join(original_dirname, new_basename_safe)

    if filename_without_ext.startswith(safe_prefix):
        if not any(contains_umlaut(p) for p in persons):
            print(f"Datei '{filepath}' ist bereits korrekt benannt und enthält keine Umlaute.")
            return False
        else:
            sorted_persons_original = sorted(list(set(persons)))
            final_prefix = f"[{', '.join(sorted_persons_original)}]_"
            new_basename_final = f"{final_prefix}{filename_without_ext}{ext}"
            new_filepath_final = os.path.join(original_dirname, new_basename_final)

            if os.path.exists(new_filepath_safe) and not os.path.exists(new_filepath_final):
                os.rename(new_filepath_safe, new_filepath_final)
                print(f"Umbenannt (final): '{new_basename_safe}' -> '{new_basename_final}'")
                return True
            else:
                print(f"Datei '{filepath}' ist bereits korrekt benannt.")
                return False

    try:
        os.rename(filepath, new_filepath_safe)
        print(f"Umbenannt (sicher): '{original_basename}' -> '{new_basename_safe}'")

        if any(contains_umlaut(p) for p in persons):
            sorted_persons_original = sorted(list(set(persons)))
            final_prefix = f"[{', '.join(sorted_persons_original)}]_"
            new_basename_final = f"{final_prefix}{filename_without_ext}{ext}"
            new_filepath_final = os.path.join(original_dirname, new_basename_final)

            if os.path.exists(new_filepath_final):
                print(
                    f"WARNUNG: Finaler Dateiname '{new_basename_final}' existiert bereits. Überspringe die finale Umbenennung.")
                return True

            os.rename(new_filepath_safe, new_filepath_final)
            print(f"Umbenannt (final): '{new_basename_safe}' -> '{new_basename_final}'")
            return True

        return True

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
    renamed_count = 0

    for dirpath, _, filenames in os.walk(ROOT_FOLDER):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                continue

            if filename.startswith('['):
                print(f"Datei '{filename}' wird übersprungen, da sie bereits umbenannt zu sein scheint.")
                continue

            persons = get_persons_from_file(filepath)

            if rename_file_with_persons(filepath, persons):
                renamed_count += 1

    print("-" * 50)
    print("Verarbeitung abgeschlossen.")
    print(f"Insgesamt wurden {renamed_count} Dateien umbenannt.")
    print("-" * 50)


if __name__ == "__main__":
    main()