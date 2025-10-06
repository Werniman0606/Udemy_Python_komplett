import os
import subprocess
import time

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.gif')


# --- KONFIGURATION ENDE ---

def check_for_incomplete_tags(file_path):
    """
    Prüft, ob eine Datei einen Namenstag, aber keine Region hat.
    Gibt True zurück, wenn ein unvollständiger Tag gefunden wird.
    """
    try:
        command = f'chcp 65001 & "{EXIFTOOL_PATH}" -XMP-MP:RegionPersonDisplayName -XMP-MP:RegionPersonRegion -T "{file_path}"'
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            check=False,
            encoding='utf-8',
            errors='ignore'
        )
        output_list = result.stdout.strip().split('\t')

        if len(output_list) == 2 and output_list[0] != '-' and output_list[1] == '-':
            print(f"⚠️ Unvollständiger Tag gefunden in: {file_path}")
            return True
        return False

    except Exception as e:
        print(f"❌ Fehler beim Prüfen der Tags für {file_path}: {e}")
        return False


def remove_digikam_tags(file_path):
    """
    Löscht alle XMP-Tags aus der Datei, indem die Datei neu aufgebaut wird.
    """
    try:
        # Erstellt eine neue Datei, wobei die gesamte XMP-Struktur ausgeschlossen wird.
        temp_file = file_path + '.temp'
        command = f'chcp 65001 & "{EXIFTOOL_PATH}" -tagsFromFile "{file_path}" -xmp:all -o "{temp_file}" "{file_path}"'
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            check=False,
            encoding='utf-8',
            errors='ignore'
        )

        if "1 image files created" in result.stdout:
            os.remove(file_path)
            os.rename(temp_file, file_path)
            print(f"✅ Tags erfolgreich gelöscht aus: {file_path}")
            return True
        else:
            print(f"❌ Fehler beim Löschen von Tags in: {file_path}")
            print(f"ExifTool-Fehlermeldung: {result.stderr.strip()}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    except Exception as e:
        print(f"❌ Fehler beim Löschen von Tags für {file_path}: {e}")
        return False



def main():
    print("Starte den Vorgang zum Löschen unvollständiger Digikam-Tags...")
    print(f"Suche nach Bildern in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Fehler: Quellverzeichnis '{SOURCE_DIR}' nicht gefunden.")
        return

    removed_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(ALLOWED_EXTENSIONS):
                if check_for_incomplete_tags(file_path):
                    if remove_digikam_tags(file_path):
                        removed_count += 1
                else:
                    print(f"➡️ Keine unvollständigen Tags gefunden in: {file_path}")

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {removed_count} Dateien bereinigt.")
    print(f"Dauer: {duration:.2f} Sekunden")


if __name__ == '__main__':
    main()