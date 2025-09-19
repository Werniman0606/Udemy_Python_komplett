import os
import subprocess
import time
import shutil
import uuid
import sys

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder\Celebrities'

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
        command_verify = f'chcp 65001 & "{EXIFTOOL_PATH}" -XMP-dc:creator -XMP-digiKam:TagsList -s3 "{file_path}"'

        result_verify = subprocess.run(
            command_verify,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
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
        os.makedirs(TEMP_DIR, exist_ok=True)

        # Erstelle einen sicheren, temporären Dateinamen (ohne Sonderzeichen)
        temp_safe_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        temp_safe_path = os.path.join(TEMP_DIR, temp_safe_filename)

        shutil.copy2(file_path, temp_safe_path)

        start_index = filename.find('[') + 1
        end_index = filename.find(']_')
        person_names_str = filename[start_index:end_index].strip()

        if not person_names_str:
            return False, "Ignoriert: Kein Name im Dateinamen gefunden."

        person_names = [name.strip() for name in person_names_str.split(',')]

        if not person_names or not person_names[0]:
            return False, "Ignoriert: Keine gültigen Namen gefunden."

        print(f"Lösche alte Tags für: '{filename}'")

        # Schreibe die Befehle in eine temporäre args-Datei
        args_file_path = os.path.join(TEMP_DIR, "tags.args")
        with open(args_file_path, "w", encoding="utf-8") as f:
            f.write("-overwrite_original_in_place\n")
            f.write("-XMP-dc:creator=\n")
            f.write("-XMP-digiKam:TagsList=\n")
            f.write("-charset filename=utf8\n")
            f.write("\n")

            for name in person_names:
                capitalized_name = name.title()
                digikam_person_tag = f"Personen/{capitalized_name}"
                f.write(f"-XMP-dc:creator+={capitalized_name}\n")
                f.write(f"-XMP-digiKam:TagsList+={digikam_person_tag}\n")

        # Führe ExifTool mit der args-Datei aus
        tag_commands = f'chcp 65001 & "{EXIFTOOL_PATH}" -@ "{args_file_path}" "{temp_safe_path}"'
        subprocess.run(tag_commands, check=True, shell=True)

        os.remove(args_file_path)

        # Nach dem Taggen sofort verifizieren
        success_verify, output_verify = verify_tags(temp_safe_path, person_names)

        if success_verify:
            # Benenne die temporäre Datei zurück in den Originalnamen
            temp_final_path = os.path.join(TEMP_DIR, filename)
            os.rename(temp_safe_path, temp_final_path)

            shutil.move(temp_final_path, file_path)
            tagged_names = ', '.join([name.title() for name in person_names])
            return True, f"✅ Erfolgreich getaggt und verifiziert mit Namen: '{tagged_names}'."
        else:
            shutil.move(temp_safe_path, file_path)
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
                print(f"{'✅' if success else '❌'} {file}: {message}")

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {tagged_count} Dateien getaggt.")
    print(f"Dauer: {duration:.2f} Sekunden")


if __name__ == '__main__':
    main()
