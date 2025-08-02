import os
import subprocess
import time

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Verzeichnis, in dem nach Bildern gesucht werden soll
BASE_DIR = r'e:\Bilder\Celebrities'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


# --- KONFIGURATION ENDE ---

def is_tag_already_present(file_path, person_name):
    """
    Prüft, ob der XMP-Tag 'People|Personenname' in einer Datei bereits vorhanden ist.
    Dabei wird die Groß- und Kleinschreibung ignoriert.
    """
    tag_to_check = f"People|{person_name}"
    command = [EXIFTOOL_PATH, '-XMP:Subject', '-s3', file_path]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False)
        if result.returncode == 0 and result.stdout:
            tags = result.stdout.strip().split('\n')
            # Prüfen, ob der Tag bereits in der Liste ist
            return any(tag.lower() == tag_to_check.lower() for tag in tags)
    except FileNotFoundError:
        print(f"❌ Fehler: ExifTool nicht gefunden unter '{EXIFTOOL_PATH}'.")
        exit()
    except Exception as e:
        print(f"⚠️ Fehler bei der Überprüfung von {file_path}: {e}")
    return False


def tag_file(file_path, person_name):
    """
    Fügt XMP-Tag 'People|Personenname' hinzu, wenn noch nicht vorhanden.
    """
    if not person_name:
        return False

    tag = f"People|{person_name}"

    if is_tag_already_present(file_path, person_name):
        return False  # Tag ist bereits vorhanden, nichts tun

    # Das += fügt den Tag hinzu, ohne bestehende Tags zu überschreiben
    command = [EXIFTOOL_PATH, f"-XMP:Subject+={tag}", file_path]

    try:
        subprocess.run(command, check=True, text=True, shell=False,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Tag '{tag}' zu '{os.path.basename(file_path)}' hinzugefügt.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Fehler beim Taggen von '{os.path.basename(file_path)}' mit '{tag}': {e.stderr.strip()}")
    except Exception as e:
        print(f"❌ Unbekannter Fehler: {e}")
    return False


def extract_person_names(filename):
    """
    Extrahiert eine Liste von Personennamen aus einem Dateinamen
    wie [Vorname1, Vorname2]_...
    """
    if filename.startswith('[') and ']_' in filename:
        end_index = filename.find(']_')
        names_string = filename[1:end_index]
        # Aufteilen des Strings am Trennzeichen ", "
        names_list = [name.strip() for name in names_string.split(',')]
        # Nur Namen zurückgeben, die nicht leer sind
        return [name for name in names_list if name]
    return []


def main():
    print("Starte den Tagging-Vorgang...")
    print(f"Suche nach Bildern im Verzeichnis: '{BASE_DIR}'")

    if not os.path.exists(BASE_DIR):
        print(f"❌ Fehler: Verzeichnis '{BASE_DIR}' wurde nicht gefunden.")
        return

    tagged_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            # Nur Dateien mit passender Endung verarbeiten
            if file.lower().endswith(ALLOWED_EXTENSIONS):
                names_to_tag = extract_person_names(file)

                # Wenn Namen gefunden wurden, die Datei taggen
                for name in names_to_tag:
                    if tag_file(file_path, name):
                        tagged_count += 1

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {tagged_count} Tags hinzugefügt.")
    print(f"Dauer: {duration:.2f} Sekunden")


if __name__ == '__main__':
    main()