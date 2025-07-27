import os
import subprocess

# Pfad zu exiftool (JETZT OHNE (-k) im Dateinamen)
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe' # <-- HIER GEÄNDERT!

# Hauptordner (Celebrities)
BASE_DIR = r'e:\Bilder\Celebrities'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')

def is_tag_already_present(file_path, person_name):
    """Prüft, ob der gegebene Personenname bereits im XMP-Subject vorhanden ist"""
    try:
        command = f'"{EXIFTOOL_PATH}" -XMP:Subject -s3 "{file_path}"'
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        tags = result.stdout.strip().split('\n')
        # Prüfen, ob der Personenname in irgendeinem der vorhandenen Tags (case-insensitiv) enthalten ist.
        # Beachten Sie, dass ExifTool bei XMP:Subject auch "tag1, tag2" zurückgeben kann,
        # daher ist es sicherer, die Tags einzeln zu überprüfen.
        return any(person_name.lower() == tag.lower() or f"people|{person_name.lower()}" == tag.lower() for tag in tags)
    except Exception as e:
        print(f"⚠️ Fehler beim Lesen von Tags für {os.path.basename(file_path)}: {e}")
        return False

def tag_file(file_path, person_name):
    """Fügt XMP-Tag 'People | Personenname' hinzu, wenn noch nicht vorhanden"""
    if is_tag_already_present(file_path, person_name):
        return

    try:
        command = f'"{EXIFTOOL_PATH}" -XMP:Subject+=People|{person_name} -overwrite_original "{file_path}"'
        # Hier ändern wir die Ausgabe von DEVNULL zu PIPE, um die tatsächliche Ausgabe zu prüfen
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE, # Ausgabe erfassen
            stderr=subprocess.PIPE, # Fehler erfassen
            text=True,
            shell=True
        )
        # Prüfen, ob der Befehl erfolgreich war (ExifTool gibt oft "1 image files updated" aus)
        if "1 image files updated" in result.stdout:
            print(f"  🏷️ Erfolgreich getaggt: {os.path.basename(file_path)} → People|{person_name}")
        else:
            # Falls ExifTool keinen Erfolg meldet, aber auch keinen Fehler über stderr
            print(f"  🤔 Tagging beendet (keine direkte Erfolgsmeldung): {os.path.basename(file_path)} (Meldung: {result.stdout.strip()})")
            if result.stderr:
                 print(f"    ExifTool-Fehlerdetails: {result.stderr.strip()}")

    except Exception as e:
        print(f"  ❌ Fehler beim Taggen von {os.path.basename(file_path)}: {e}")

def extract_person_name(filename):
    """Extrahiert den Personennamen aus einem Dateinamen wie [Vorname Nachname]_..."""
    if filename.startswith('[') and ']_' in filename:
        end_index = filename.find(']_')
        return filename[1:end_index]
    return None

def main():
    print(f"\n🔍 Starte Durchlauf im Verzeichnis:\n{BASE_DIR}\n")

    for root, dirs, files in os.walk(BASE_DIR):
        print(f"📁 Durchsuche Ordner: {root}")
        for file in files:
            # NEUE ZEILE: Ausgabe jeder bearbeiteten Datei
            print(f"  Verarbeite Datei: {os.path.basename(file)}")

            if file.lower().endswith(ALLOWED_EXTENSIONS):
                person_name = extract_person_name(file)
                if person_name:
                    file_path = os.path.join(root, file)
                    tag_file(file_path, person_name)
                else:
                    print(f"  ➡️ Überspringe '{os.path.basename(file)}': Kein Personenname im Dateinamen gefunden.")
            else:
                print(f"  ➡️ Überspringe '{os.path.basename(file)}': Keine erlaubte Dateierweiterung.")

    print("\n✅ Vorgang abgeschlossen.")

if __name__ == '__main__':
    main()