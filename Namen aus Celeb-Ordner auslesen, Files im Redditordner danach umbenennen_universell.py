# ==============================================================================
# Dateiname: download_name_matcher.py
# Beschreibung: Liest gültige Personennamen aus dem Master-Ordner und wendet sie
#                als [Name]_Präfix auf übereinstimmende Dateinamen im Download-Ordner an.
#
# Funktioniert nativ unter Windows UND Linux (CachyOS).
# ==============================================================================

import os
import re
import subprocess
from pathlib import Path

# --- KONFIGURATION & BETRIEBSSYSTEM-ERKENNUNG ---
if os.name == 'nt':  # Windows
    MASTER_FOLDER = Path(r'e:\Bilder\Celebrities')
    DOWNLOAD_FOLDER = Path(r'd:\Bilder')
    EXIFTOOL_PATH = Path(r'd:\exiftool-13.52_64\exiftool-13.52_64\exiftool.exe')
else:  # Linux (CachyOS)
    MASTER_FOLDER = Path("/run/media/marcoj/Laufwerk E/Bilder/Celebrities")
    DOWNLOAD_FOLDER = Path("/run/media/marcoj/Laufwerk E/Bilder/Celebrities/Playboy")
    EXIFTOOL_PATH = Path("/usr/bin/exiftool")
    # Falls es dort nicht liegt, Standardfall für den globalen Aufruf:
    if not EXIFTOOL_PATH.exists():
        EXIFTOOL_PATH = Path("exiftool")

# Dateitypen, die verarbeitet werden sollen
FILE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.tif', '.gif', '.webp')

# Das Metadatenfeld für allgemeine Tags (XMP:Subject)
PERSONEN_TAG_FELD = 'XMP:Subject'


# --- FUNKTIONEN ---

def collect_master_names(master_dir):
    """Sammelt alle gültigen Personennamen aus den Unterordnern der Master-Sammlung."""
    valid_names = set()
    print("1. Sammle gültige Namen aus der Master-Sammlung...")

    # Bestimme, wie viele Ebenen der Master-Ordner selbst hat
    master_depth = len(master_dir.parts)

    # os.walk akzeptiert Path-Objekte, root konvertieren wir direkt in ein Path-Objekt
    for root_str, dirnames, _ in os.walk(master_dir):
        root = Path(root_str)

        # Wir wollen nur Ordner, die direkt unterhalb des Initialen-Ordners liegen
        # Struktur: Master / Initial (z.B. A) / Person -> Also master_depth + 2
        if root != master_dir and len(root.parts) > master_depth:
            for dirname in dirnames:
                valid_names.add(dirname)

    print(f"   -> {len(valid_names)} gültige Personennamen gefunden.")
    return valid_names


def find_and_rename_files(download_dir, valid_names):
    """Durchsucht den Download-Ordner und benennt übereinstimmende Dateien um."""
    print(f"\n2. Starte Namens-Matching und Umbenennung in {download_dir}...")
    renamed_count = 0
    tagged_count = 0

    # Namen für die Suche vorbereiten: Längere Namen zuerst prüfen!
    sorted_names = sorted(list(valid_names), key=len, reverse=True)

    # Durchlaufe den Zielordner rekursiv mit rglob
    for file_path in download_dir.rglob('*'):
        # Nur Dateien mit passender Endung verarbeiten
        if not file_path.is_file() or file_path.suffix.lower() not in FILE_EXTENSIONS:
            continue

        filename = file_path.name

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
            new_prefix = f'[{best_match}]_'
            new_filename = new_prefix + filename
            new_path = file_path.parent / new_filename

            # --- A: Umbenennen ---
            try:
                file_path.rename(new_path)
                print(f"   ✅ UMBENANNT: {filename} -> {new_filename}")
                renamed_count += 1
                file_to_tag = new_path
            except FileExistsError:
                print(f"   ⚠️ Überspringe Umbenennung: Ziel {new_filename} existiert bereits.")
                continue
            except OSError as e:
                print(f"   ❌ Fehler beim Umbenennen von {filename}: {e}")
                continue

            # --- B: Metadaten-Tags schreiben ---
            command = [
                f"-{PERSONEN_TAG_FELD}+={best_match}",
                f"-MWG-RS:Name+={best_match}",
                '-overwrite_original'
            ]
            full_command = [str(EXIFTOOL_PATH), '-m'] + command + [str(file_to_tag)]

            try:
                # ExifTool ausführen
                subprocess.run(full_command, capture_output=True, text=True, check=True)
                tagged_count += 1
            except subprocess.CalledProcessError as e:
                print(f"   ❌ FEHLER beim Tagging von {new_filename}: {e.stderr.strip()}")
            except FileNotFoundError:
                print(f"   ❌ FEHLER: ExifTool nicht gefunden. Abbruch des Taggings.")
                return renamed_count, tagged_count

    return renamed_count, tagged_count


# --- HAUPTPROGRAMM ---

if __name__ == "__main__":
    if not MASTER_FOLDER.is_dir():
        print(f"❌ Fehler: Master-Ordner '{MASTER_FOLDER}' existiert nicht.")
        exit()
    if not DOWNLOAD_FOLDER.is_dir():
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