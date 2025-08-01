import os
import subprocess
import shutil

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Quell- und Zielverzeichnis
SOURCE_DIR = r'e:\Bilder'
DESTINATION_DIR = r'e:\Bilder-getaggt'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


# --- KONFIGURATION ENDE ---

def has_people_tag(file_path):
    """Prüft, ob eine Datei den XMP-Tag 'People|...' enthält."""
    try:
        command = [EXIFTOOL_PATH, '-XMP:Subject', '-s3', file_path]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        if result.returncode == 0 and result.stdout:
            tags = result.stdout.strip().split('\n')
            # Prüft, ob einer der Tags mit 'People|' beginnt
            return any(tag.lower().startswith('people|') for tag in tags)
    except Exception as e:
        print(f"⚠️ Fehler beim Lesen von Tags für {file_path}: {e}")
    return False


def main():
    print(f"\n🔍 Starte den Scan von '{SOURCE_DIR}' nach Bildern mit People-Tags.\n")

    if not os.path.isdir(SOURCE_DIR):
        print(f"❌ Fehler: Das Quellverzeichnis '{SOURCE_DIR}' existiert nicht.")
        return

    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
        print(f"📦 Zielverzeichnis '{DESTINATION_DIR}' wurde erstellt.")

    count_moved = 0
    count_skipped = 0

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(ALLOWED_EXTENSIONS):
                source_path = os.path.join(root, file)

                if has_people_tag(source_path):
                    # Relative Pfade erstellen, um die Ordnerstruktur zu erhalten
                    relative_path = os.path.relpath(source_path, SOURCE_DIR)
                    destination_path = os.path.join(DESTINATION_DIR, relative_path)

                    # Überprüfen und erstellen des Zielverzeichnisses
                    destination_dir = os.path.dirname(destination_path)
                    if not os.path.exists(destination_dir):
                        os.makedirs(destination_dir, exist_ok=True)

                    try:
                        shutil.move(source_path, destination_path)
                        print(f"✅ Verschiebe: '{source_path}' -> '{destination_path}'")
                        count_moved += 1
                    except Exception as e:
                        print(f"❌ Fehler beim Verschieben von '{source_path}': {e}")
                else:
                    print(f"➡️ Überspringe '{os.path.basename(file)}': Kein passender Tag gefunden.")
                    count_skipped += 1

    print("\n---")
    print(f"✅ Vorgang abgeschlossen.")
    print(f"📊 {count_moved} Bilder wurden verschoben.")
    print(f"📊 {count_skipped} Bilder wurden übersprungen.")


if __name__ == '__main__':
    main()