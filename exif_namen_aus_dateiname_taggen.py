# ==============================================================================
# Dateiname Vorschlag (Deutsch): exif_namen_aus_dateiname_taggen.py
# Dateiname Vorschlag (Technisch): exiftool_name_tagger_with_verification.py
#
# Beschreibung: Dieses Skript automatisiert das Schreiben von XMP-Tags (Metadaten)
#               in Bilddateien (JPG/JPEG). Es extrahiert Personennamen aus dem
#               Dateipräfix, das im Format "[Name1, Name2]_" vorliegt, und schreibt
#               diese Namen als XMP-dc:creator und XMP-digiKam:TagsList.
#               Es verwendet eine temporäre Datei und eine Args-Datei für
#               ExifTool, um mit Sonderzeichen und Leerzeichen umzugehen.
#               Nach dem Tagging erfolgt eine sofortige Verifizierung der Tags.
# ==============================================================================

import os
import subprocess
import time
import shutil
import uuid
import sys
import re  # Obwohl re nicht direkt im Code verwendet wird, ist es für die Logik relevant

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder\Celebrities\S\Swetlana Loeper'

# Temporäres Verzeichnis für die Verarbeitung (erforderlich für sicheres Tagging)
TEMP_DIR = r'e:\temp_exiftool'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg')


# --- KONFIGURATION ENDE ---

def verify_tags(file_path, person_names):
    """
    Überprüft, ob die Tags für alle Personen in der Datei vorhanden sind,
    indem es die Ausgaben von XMP-dc:creator und XMP-digiKam:TagsList liest.
    """
    try:
        # chcp 65001 stellt sicher, dass die Windows-Konsole UTF-8-Ausgabe korrekt verarbeitet
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

        # Prüfe, ob jeder Name (in Titel-Schreibweise) im ExifTool-Output vorkommt
        for name in person_names:
            capitalized_name = name.title()
            if capitalized_name not in output:
                return False, output

        return True, output

    except Exception as e:
        return False, f"❌ Fehler bei der Verifizierung für '{file_path}': {e}"


def tag_file_with_person_names(file_path):
    """
    Extrahiert Personennamen aus dem Dateinamen, schreibt die XMP-Tags und verifiziert.
    """
    filename = os.path.basename(file_path)

    # Prüft, ob der Dateiname dem erwarteten Format '[...]_' entspricht
    if not filename.startswith('[') or ']_' not in filename:
        return False, "Ignoriert: Dateiname entspricht nicht dem Muster."

    try:
        os.makedirs(TEMP_DIR, exist_ok=True)

        # 1. Temporäre Kopie erstellen, um das Risiko bei der ExifTool-Verarbeitung zu minimieren
        temp_safe_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
        temp_safe_path = os.path.join(TEMP_DIR, temp_safe_filename)

        shutil.copy2(file_path, temp_safe_path)

        # 2. Namen aus dem Präfix extrahieren
        start_index = filename.find('[') + 1
        end_index = filename.find(']_')
        person_names_str = filename[start_index:end_index].strip()

        if not person_names_str:
            return False, "Ignoriert: Kein Name im Dateinamen gefunden."

        # Teilt die Namen, falls mehrere durch Kommas getrennt sind
        person_names = [name.strip() for name in person_names_str.split(',')]

        if not person_names or not person_names[0]:
            return False, "Ignoriert: Keine gültigen Namen gefunden."

        print(f"Lösche alte Tags für: '{filename}'")

        # 3. ExifTool-Befehle in eine temporäre Args-Datei schreiben (sicherer Umgang mit UTF-8/Sonderzeichen)
        args_file_path = os.path.join(TEMP_DIR, "tags.args")
        with open(args_file_path, "w", encoding="utf-8") as f:
            f.write("-overwrite_original_in_place\n")  # Originaldatei wird überschrieben
            f.write("-XMP-dc:creator=\n")  # Löscht vorhandene Autoren-Tags
            f.write("-XMP-digiKam:TagsList=\n")  # Löscht vorhandene DigiKam-Tags
            f.write("-charset filename=utf8\n")  # Sicherstellen, dass Dateinamen korrekt gelesen werden
            f.write("\n")

            # Fügt für jeden gefundenen Namen die Tags hinzu
            for name in person_names:
                capitalized_name = name.title()  # Erster Buchstabe groß (Standard für Namen)
                digikam_person_tag = f"Personen/{capitalized_name}"
                f.write(f"-XMP-dc:creator+={capitalized_name}\n")  # Fügt Author hinzu
                f.write(f"-XMP-digiKam:TagsList+={digikam_person_tag}\n")  # Fügt DigiKam-Tag hinzu

        # 4. ExifTool mit der Args-Datei auf die temporäre Datei anwenden
        tag_commands = f'chcp 65001 & "{EXIFTOOL_PATH}" -@ "{args_file_path}" "{temp_safe_path}"'
        subprocess.run(tag_commands, check=True, shell=True)

        os.remove(args_file_path)

        # 5. Verifizieren und Originaldatei ersetzen
        success_verify, output_verify = verify_tags(temp_safe_path, person_names)

        if success_verify:
            # Benenne die temporäre Datei zurück in den Originalnamen (falls notwendig)
            temp_final_path = os.path.join(TEMP_DIR, filename)
            os.rename(temp_safe_path, temp_final_path)

            # Verschiebe die fertige Datei zurück an ihren ursprünglichen Ort
            shutil.move(temp_final_path, file_path)
            tagged_names = ', '.join([name.title() for name in person_names])
            return True, f"✅ Erfolgreich getaggt und verifiziert mit Namen: '{tagged_names}'."
        else:
            # Falls die Verifizierung fehlschlägt, die temporäre Datei löschen (oder zurückverschieben)
            shutil.move(temp_safe_path, file_path)
            tagged_names = ', '.join([name.title() for name in person_names])
            return False, f"❌ Tags konnten nicht korrekt verifiziert werden für '{tagged_names}'. Gefundene Tags: {output_verify}"

    except FileNotFoundError:
        # Aufräumarbeiten für den Fehlerfall (falls temp-Datei noch da)
        if os.path.exists(temp_safe_path):
            os.remove(temp_safe_path)
        return False, f"Fehler: Exiftool nicht gefunden unter '{EXIFTOOL_PATH}'."
    except subprocess.CalledProcessError as e:
        if os.path.exists(temp_safe_path):
            os.remove(temp_safe_path)
        error_output = e.stderr.strip() if e.stderr else "Unbekannter Fehler von ExifTool."
        return False, f"Exiftool-Fehler beim Taggen: {error_output}"
    except Exception as e:
        if os.path.exists(temp_safe_path):
            os.remove(temp_safe_path)
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
    # Stellt sicher, dass das temporäre Verzeichnis nach Abschluss gelöscht wird (falls es leer ist)
    try:
        if os.path.exists(TEMP_DIR) and not os.listdir(TEMP_DIR):
            os.rmdir(TEMP_DIR)
        print(f"Das temporäre Verzeichnis {TEMP_DIR} wurde aufgeräumt (falls leer).")
    except Exception as e:
        print(f"Warnung: Temporäres Verzeichnis {TEMP_DIR} konnte nicht entfernt werden: {e}")

    main()