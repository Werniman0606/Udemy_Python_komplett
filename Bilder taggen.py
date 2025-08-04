import os
import subprocess
import time
import shutil

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder2'

# Temporäres Verzeichnis für die Verarbeitung
TEMP_DIR = r'e:\temp_exiftool'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg')

# --- KONFIGURATION ENDE ---

def verify_tags(file_path, person_names):
    """
    Überprüft, ob die Tags für alle Personen in der Datei vorhanden sind.
    """
    try:
        command_verify = [
            EXIFTOOL_PATH,
            '-XMP-dc:creator',
            '-XMP-digiKam:TagsList',
            '-s3',
            file_path
        ]

        result_verify = subprocess.run(
            command_verify,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            encoding='utf-8',
            errors='ignore'
        )

        output = result_verify.stdout.strip() if result_verify.stdout else ""

        for name in person_names:
            capitalized_name = name.title()
            if capitalized_name not in output:
                return False, output

        return True, output

    except Exception as e:
        return False, f"❌ Fehler bei der Verifizierung für '{file_path}': {e}"


def tag_file_with_person_names(file_path):
    """
    Extrahiert Personennamen aus dem Dateinamen und setzt die XMP-Tags.
    """
    filename = os.path.basename(file_path)

    if not filename.startswith('[') or ']_' not in filename:
        return False, "Ignoriert: Dateiname entspricht nicht dem Muster."

    try:
        # Erstelle temporäres Verzeichnis, falls es nicht existiert
        os.makedirs(TEMP_DIR, exist_ok=True)
        temp_file_path = os.path.join(TEMP_DIR, filename)
        shutil.copy2(file_path, temp_file_path)

        start_index = filename.find('[') + 1
        end_index = filename.find(']_')
        person_names_str = filename[start_index:end_index].strip()

        if not person_names_str:
            return False, "Ignoriert: Kein Name im Dateinamen gefunden."

        person_names = [name.strip() for name in person_names_str.split(',')]

        if not person_names or not person_names[0]:
            return False, "Ignoriert: Keine gültigen Namen gefunden."

        print(f"Lösche alte Tags für: '{filename}'")
        # Tags leeren
        command_delete = [
            EXIFTOOL_PATH,
            '-overwrite_original_in_place',
            '-XMP-dc:creator=',
            '-XMP-digiKam:TagsList=',
            '-charset', 'filename=utf8', # Kodierung für Dateinamen erzwingen
            temp_file_path
        ]
        subprocess.run(command_delete, check=True)

        # Tags für jede Person sammeln
        tag_commands = [
            EXIFTOOL_PATH,
            '-overwrite_original_in_place',
            '-charset', 'filename=utf8'
        ]

        for name in person_names:
            capitalized_name = name.title()
            digikam_person_tag = f"Personen/{capitalized_name}"

            tag_commands.extend([
                f'-XMP-dc:creator+={capitalized_name}',
                f'-XMP-digiKam:TagsList+={digikam_person_tag}',
            ])

        # Tags in einem einzigen Befehl hinzufügen
        tag_commands.append(temp_file_path)
        subprocess.run(tag_commands, check=True)

        # Nach dem Taggen sofort verifizieren
        success_verify, output_verify = verify_tags(temp_file_path, person_names)

        if success_verify:
            shutil.move(temp_file_path, file_path) # Bearbeitete Datei zurück verschieben
            tagged_names = ', '.join([name.title() for name in person_names])
            return True, f"Erfolgreich getaggt und verifiziert mit Namen: '{tagged_names}'."
        else:
            shutil.move(temp_file_path, file_path) # Originaldatei zurück verschieben
            tagged_names = ', '.join([name.title() for name in person_names])
            return False, f"❌ Tags konnten nicht korrekt verifiziert werden für '{tagged_names}'. Gefundene Tags: {output_verify}"

    except FileNotFoundError:
        return False, f"Fehler: Exiftool nicht gefunden unter '{EXIFTOOL_PATH}'."
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip() if e.stderr else "Unbekannter Fehler von ExifTool."
        return False, f"Exiftool-Fehler beim Taggen: {error_output}"
    except Exception as e:
        return False, f"Unerwarteter Fehler beim Taggen: {e}"

def main():
    print("Starte den Tagging-Vorgang für Bilder...")
    print(f"Durchsuche Ordner: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Fehler: Quellverzeichnis '{SOURCE_DIR}' nicht gefunden.")
        return

    if not os.path.isfile(EXIFTOOL_PATH):
        print(f"❌ Fehler: Exiftool-Pfad '{EXIFTOOL_PATH}' ist ungültig. Skript wird beendet.")
        return

    tagged_count = 0
    start_time = time.time()

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)

            if file.lower().endswith(ALLOWED_EXTENSIONS):
                success, message = tag_file_with_person_names(file_path)
                if success:
                    tagged_count += 1
                    print(f"✅ {file}: {message}")
                else:
                    print(f"❌ {file}: {message}")

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {tagged_count} Dateien getaggt.")
    print(f"Dauer: {duration:.2f} Sekunden")

if __name__ == '__main__':
    main()