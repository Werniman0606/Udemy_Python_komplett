# ==============================================================================
# Dateiname: download_name_matcher.py
# Beschreibung: Liest gültige Personennamen aus dem Master-Ordner und wendet sie
#               als [Name]_Präfix auf übereinstimmende Dateinamen im Download-Ordner an.
# ==============================================================================

import os
import re
import subprocess
from collections import defaultdict

# --- KONFIGURATION ---

# 1. QUELLE der gültigen Personennamen (Master-Sammlung)
MASTER_FOLDER = r'e:\Bilder\Celebrities'

# 2. ZIELORDNER der Umbenennung (Downloads mit unsortierten Dateien)
DOWNLOAD_FOLDER = r'd:\Bilder'

# PFAD ZU EXIFTOOL.EXE (Wird hier nur für die Metadaten-Schreibfunktion benötigt)
EXIFTOOL_PATH = r'd:\exiftool-13.52_64\exiftool-13.52_64\exiftool.exe'

# Dateitypen, die verarbeitet werden sollen
FILE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.tif','.gif','.png')

# Das Metadatenfeld für allgemeine Tags (XMP:Subject)
PERSONEN_TAG_FELD = 'XMP:Subject'


# --- FUNKTIONEN ---

def collect_master_names(master_dir):
    """Sammelt alle gültigen Personennamen aus den Unterordnern der Master-Sammlung."""
    valid_names = set()
    print("1. Sammle gültige Namen aus der Master-Sammlung...")

    # Durchlaufe rekursiv alle Ordner
    for dirpath, dirnames, _ in os.walk(master_dir):
        # Wir sind nur an den untersten Ordnernamen interessiert, die eine Person darstellen
        # Wir überspringen den ROOT_FOLDER selbst
        if dirpath != master_dir and len(dirpath.split(os.sep)) > len(master_dir.split(os.sep)):
            # Der Name ist der letzte Teil des Pfades
            person_name = os.path.basename(dirpath)
            valid_names.add(person_name)

    print(f"   -> {len(valid_names)} gültige Personennamen gefunden.")
    return valid_names


def find_and_rename_files(download_dir, valid_names):
    """Durchsucht den Download-Ordner und benennt übereinstimmende Dateien um."""
    print(f"\n2. Starte Namens-Matching und Umbenennung in {download_dir}...")
    renamed_count = 0
    tagged_count = 0

    # Namen für die Suche vorbereiten: Längere Namen zuerst prüfen!
    # ("Bonnie Tyler" muss vor "Tyler" geprüft werden, falls "Tyler" auch ein Name wäre)
    sorted_names = sorted(list(valid_names), key=len, reverse=True)

    # Erstelle ein Regex-Pattern für die Suche (ignoriert Groß-/Kleinschreibung und erlaubt Leerzeichen/Unterstriche)
    # WICHTIG: Erlaubt nur Alpha-Zeichen, um False Positives zu minimieren

    # Erstellt ein Diktionär {Namensteil_Klein: Name_Originalschreibweise}
    # Dies ist effizienter als eine Liste
    name_lookup = {name.lower(): name for name in valid_names}

    for dirpath, _, filenames in os.walk(download_dir):
        for filename in filenames:
            if not filename.lower().endswith(FILE_EXTENSIONS):
                continue

            # Prüfe, ob die Datei bereits das korrekte Präfix hat, um Doppelverarbeitung zu vermeiden
            if re.match(r'^\[.+?\]_', filename):
                continue

            best_match = None

            # Normalisiere den Dateinamen für die Suche (Kleinbuchstaben, ersetzt Leerzeichen/Unterstriche)
            search_filename = filename.lower().replace('_', ' ').replace('-', ' ')

            # 3. Finde das beste Match im Dateinamen
            for original_name in sorted_names:
                search_term = original_name.lower()

                # Suche nach dem vollen Namen als Wortgrenze
                if re.search(r'\b' + re.escape(search_term) + r'\b', search_filename):
                    best_match = original_name
                    break  # Längstes und bestes Match gefunden

            # 4. Umbenennung und Tagging, falls ein Match gefunden wurde
            if best_match:
                old_path = os.path.join(dirpath, filename)
                new_prefix = f'[{best_match}]_'
                new_filename = new_prefix + filename
                new_path = os.path.join(dirpath, new_filename)

                # --- A: Umbenennen ---
                try:
                    os.rename(old_path, new_path)
                    print(f"  ✅ UMBENANNT: {filename} -> {new_filename}")
                    renamed_count += 1
                    file_to_tag = new_path
                except FileExistsError:
                    print(f"  ⚠️ Überspringe Umbenennung: Ziel {new_filename} existiert bereits.")
                    continue
                except OSError as e:
                    print(f"  ❌ Fehler beim Umbenennen von {filename}: {e}")
                    continue

                # --- B: Metadaten-Tags schreiben ---
                # Füge den Personennamen zu XMP:Subject und MWG-RS:Name hinzu
                command = [
                    f"-{PERSONEN_TAG_FELD}+={best_match}",
                    f"-MWG-RS:Name+={best_match}",
                    '-overwrite_original'
                ]
                full_command = [EXIFTOOL_PATH, '-m'] + command + [file_to_tag]

                try:
                    subprocess.run(full_command, capture_output=True, text=True, check=True)
                    tagged_count += 1
                except subprocess.CalledProcessError as e:
                    print(f"  ❌ FEHLER beim Tagging von {new_filename}: {e.stderr.strip()}")
                except FileNotFoundError:
                    print(f"  ❌ FEHLER: ExifTool nicht gefunden. Abbruch des Taggings.")
                    return renamed_count, tagged_count

    return renamed_count, tagged_count


# --- HAUPTPROGRAMM ---

if __name__ == "__main__":
    if not os.path.isdir(MASTER_FOLDER):
        print(f"❌ Fehler: Master-Ordner '{MASTER_FOLDER}' existiert nicht.")
        exit()
    if not os.path.isdir(DOWNLOAD_FOLDER):
        print(f"❌ Fehler: Download-Ordner '{DOWNLOAD_FOLDER}' existiert nicht.")
        exit()

    # 1. Master-Namen sammeln
    master_names = collect_master_names(MASTER_FOLDER)

    if not master_names:
        print("Keine Personennamen im Master-Ordner gefunden. Abbruch.")
        exit()

    print("\n" + "=" * 50)
    input(f"Starte Umbenennung in {DOWNLOAD_FOLDER}. Mit ENTER bestätigen.")
    print("=" * 50)

    # 2. Matching und Umbenennung durchführen
    renamed, tagged = find_and_rename_files(DOWNLOAD_FOLDER, master_names)

    print("\n========================================================")
    print("🏁 Prozess abgeschlossen.")
    print(f"Dateien umbenannt: {renamed}")
    print(f"Metadaten-Tags hinzugefügt: {tagged}")
    print("========================================================")