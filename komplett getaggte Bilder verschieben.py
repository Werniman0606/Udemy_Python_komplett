import os
import subprocess
import shutil
import time

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder'

# Zielverzeichnis, in das die getaggten Dateien verschoben werden sollen
DEST_DIR = r'e:\Bilder-getaggt'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


# --- KONFIGURATION ENDE ---

def get_tag_counts(file_path):
    """
    Zählt die Anzahl der Gesichtsregionen und getaggten Personen mit einem robusteren Befehl.
    """
    try:
        # Fragen Sie alle relevanten Tags ab
        command = f'chcp 65001 & "{EXIFTOOL_PATH}" -XMP-MP:RegionPersonDisplayName -XMP-dc:creator -T "{file_path}"'

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

        region_count = 0
        creator_count = 0

        # Die Regionen-Ausgabe ist der erste Eintrag
        if len(output_list) > 0 and output_list[0] and output_list[0] != '-':
            region_count = output_list[0].count(',') + 1

        # Der Creator-Tag ist der zweite Eintrag
        if len(output_list) > 1 and output_list[1] and output_list[1] != '-':
            creator_count = output_list[1].count(',') + 1

        return region_count, creator_count

    except Exception as e:
        print(f"⚠️ Fehler beim Lesen von Tags für {file_path}: {e}")
        return 0, 0


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
    print("Starte den Verschiebe-Vorgang für vollständig getaggte Bilder...")
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
                region_count, creator_count = get_tag_counts(file_path)

                # Neue Bedingung: Es muss mindestens einen Creator-Tag geben
                # UND die Anzahl der Regionen muss mit der Anzahl der Tags übereinstimmen.
                if creator_count > 0 and region_count == creator_count:
                    if move_file(file_path, DEST_DIR):
                        print(
                            f"✅ Verschiebe: {file_path} (Regionen: {region_count}, Tags: {creator_count})")
                        moved_count += 1
                else:
                    print(f"➡️ Überspringe: {file_path} (Regionen: {region_count}, Tags: {creator_count})")

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {moved_count} Dateien verschoben.")
    print(f"Dauer: {duration:.2f} Sekunden")


if __name__ == '__main__':
    main()