import os
import subprocess
import shutil
import time

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder    '

# Zielverzeichnis, in das die getaggten Dateien verschoben werden sollen
DEST_DIR = r'e:\Bilder-getaggt'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


# --- KONFIGURATION ENDE ---

def has_person_tags(file_path):
    """
    Prüft, ob eine Datei den XMP-Tag 'XMP-digiKam:TagsList' mit "Personen/" enthält.
    """
    try:
        command = [
            EXIFTOOL_PATH,
            '-XMP-digiKam:TagsList',
            '-s3',
            file_path
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        output = result.stdout.strip()
        # Überprüfen, ob der Tag-Output mit "Personen/" beginnt.
        return output.lower().startswith('personen/')

    except subprocess.CalledProcessError as e:
        # Exiftool gibt einen Fehlercode zurück, wenn keine Tags gefunden werden.
        return False
    except Exception as e:
        print(f"⚠️ Fehler beim Lesen von Tags für {file_path}: {e}")
        return False


def move_file(source_path, dest_base_dir):
    """
    Verschiebt eine Datei und behält dabei die ursprüngliche Verzeichnisstruktur bei.
    """
    relative_path = os.path.relpath(source_path, SOURCE_DIR)
    dest_path = os.path.join(dest_base_dir, relative_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        shutil.move(source_path, dest_path)
        return True
    except Exception as e:
        print(f"❌ Fehler beim Verschieben von '{source_path}' nach '{dest_path}': {e}")
        return False


def main():
    print("Starte den Verschiebe-Vorgang für getaggte Dateien...")
    print(f"Suche nach Bildern in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Fehler: Quellverzeichnis '{SOURCE_DIR}' nicht gefunden.")
        return

    if not os.path.exists(DEST_DIR):
        print(f"⚠️ Zielverzeichnis '{DEST_DIR}' existiert nicht. Es wird erstellt.")
        os.makedirs(DEST_DIR, exist_ok=True)

    moved_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)

            if file.lower().endswith(ALLOWED_EXTENSIONS):
                if has_person_tags(file_path):
                    if move_file(file_path, DEST_DIR):
                        print(
                            f"✅ Verschiebe: {file_path} -> {os.path.join(DEST_DIR, os.path.relpath(file_path, SOURCE_DIR))}")
                        moved_count += 1

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {moved_count} Dateien verschoben.")
    print(f"Dauer: {duration:.2f} Sekunden")


if __name__ == '__main__':
    main()