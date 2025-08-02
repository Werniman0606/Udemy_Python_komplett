import os
import subprocess
import shutil
import time

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder\Celebrities'

# Zielverzeichnis, in das die getaggten Dateien verschoben werden sollen
DEST_DIR = r'e:\Bilder-getaggt'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


# --- KONFIGURATION ENDE ---

def has_people_tag(file_path):
    """
    Prüft, ob eine Datei den XMP-Tag 'People|...' enthält.

    Args:
        file_path (str): Der vollständige Pfad zur Bilddatei.

    Returns:
        bool: True, wenn ein People-Tag gefunden wurde, sonst False.
    """
    try:
        command = [EXIFTOOL_PATH, '-XMP:Subject', '-s3', file_path]
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False,
            check=True
        )
        if result.stdout:
            # Trennen der Tags an Kommas und Leerzeichen, um alle Tags zu prüfen
            tags = result.stdout.strip().split(',')

            # Prüfen, ob irgendein Tag mit "People|" beginnt
            for tag in tags:
                if tag.strip().lower().startswith('people|'):
                    return True
    except subprocess.CalledProcessError as e:
        # Exiftool gibt einen Fehlercode zurück, wenn keine Tags gefunden werden.
        # Dies ist kein Problem, sondern erwartetes Verhalten.
        pass
    except Exception as e:
        print(f"⚠️ Fehler beim Lesen von Tags für {file_path}: {e}")
    return False


def move_file(source_path, dest_base_dir):
    """
    Verschiebt eine Datei und behält dabei die ursprüngliche Verzeichnisstruktur bei.

    Args:
        source_path (str): Der vollständige Pfad der Quelldatei.
        dest_base_dir (str): Das Basisverzeichnis, in das verschoben werden soll.

    Returns:
        bool: True, wenn die Datei erfolgreich verschoben wurde, sonst False.
    """
    # Relative Pfadstruktur vom SOURCE_DIR zum Dateinamen erhalten
    relative_path = os.path.relpath(source_path, SOURCE_DIR)

    # Vollständiger Zielpfad erstellen
    dest_path = os.path.join(dest_base_dir, relative_path)

    # Zielverzeichnis erstellen, falls es noch nicht existiert
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

    moved_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            # Wichtige Optimierung: Nur Dateien mit der passenden Namenskonvention prüfen
            if file.startswith('[') and file.lower().endswith(ALLOWED_EXTENSIONS):
                file_path = os.path.join(root, file)

                # Prüfen, ob der Datei ein People-Tag zugewiesen wurde
                if has_people_tag(file_path):
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