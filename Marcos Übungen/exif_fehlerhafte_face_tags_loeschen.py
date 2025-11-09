# ==============================================================================
# Dateiname Vorschlag (Deutsch): exif_fehlerhafte_face_tags_loeschen.py
# Dateiname Vorschlag (Technisch): exiftool_incomplete_tag_cleaner.py
#
# Beschreibung: Dieses Skript durchsucht rekursiv ein Verzeichnis nach Bildern
#               und identifiziert "unvollständige" Personen-Tags. Diese treten auf,
#               wenn ein Personenname (XMP-MP:RegionPersonDisplayName) gespeichert ist,
#               aber die zugehörige Gesichtsregion/Koordinate
#               (XMP-MP:RegionPersonRegion) fehlt.
#               Um die Inkonsistenz zu beheben, wird die gesamte XMP-Struktur
#               aus der betroffenen Datei entfernt und die Datei neu geschrieben.
#               Dies ist eine radikale, aber effektive Methode zur Bereinigung
#               fehlerhafter Metadaten.
# ==============================================================================

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
    Prüft, ob eine Datei einen Namenstag (DisplayName), aber keine Region (Region) hat.
    Gibt True zurück, wenn ein unvollständiger Tag gefunden wird.
    """
    try:
        # Fragt explizit nach beiden Tags im Tabulator-getrennten Format (-T).
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

        # Logik für unvollständigen Tag: DisplayName ist vorhanden ('-') UND Region ist NICHT vorhanden ('-')
        if len(output_list) == 2 and output_list[0].strip() != '-' and output_list[1].strip() == '-':
            # Umfassendere Prüfung: Überprüfen, ob die tatsächlichen Listenlängen übereinstimmen müssten
            # (Dieser Ansatz ist einfacher und deckt den häufigsten Fehlerfall ab)
            print(f"⚠️ UNVOLLSTÄNDIGER TAG gefunden in: {file_path}")
            return True
        return False

    except Exception as e:
        print(f"❌ Fehler beim Prüfen der Tags für {file_path}: {e}")
        return False


def remove_digikam_tags(file_path):
    """
    Löscht ALLE XMP-Tags aus der Datei, indem die Datei neu aufgebaut wird
    (kopiert alle Tags außer XMP in eine temporäre Datei und benennt um).
    """
    try:
        # Erstellt eine neue Datei, wobei die gesamte XMP-Struktur ausgeschlossen wird.
        temp_file = file_path + '.temp'
        # -tagsFromFile liest alle Tags; -xmp:all schließt explizit alle XMP-Tags aus
        command = f'chcp 65001 & "{EXIFTOOL_PATH}" -tagsFromFile "{file_path}" -XMP:All= -o "{temp_file}" "{file_path}"'
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

        # Prüfen, ob ExifTool die neue Datei erfolgreich erstellt hat
        if "1 image files created" in result.stdout:
            # Originaldatei löschen und temporäre Datei umbenennen
            os.remove(file_path)
            os.rename(temp_file, file_path)
            print(f"✅ XMP-Tags erfolgreich gelöscht und Datei bereinigt: {file_path}")
            return True
        else:
            print(f"❌ Fehler beim Löschen von Tags in: {file_path}")
            print(f"ExifTool-Fehlermeldung: {result.stderr.strip()}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    except Exception as e:
        print(f"❌ Unerwarteter Fehler beim Löschen von Tags für {file_path}: {e}")
        return False


def main():
    print("Starte den Vorgang zum Löschen unvollständiger Digikam-Tags...")
    print(f"Suche nach Bildern in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Fehler: Quellverzeichnis '{SOURCE_DIR}' nicht gefunden.")
        return

    # Sicherheitsprüfung für Exiftool
    if not os.path.isfile(EXIFTOOL_PATH):
        print(f"❌ Fehler: Exiftool-Pfad '{EXIFTOOL_PATH}' ist ungültig. Skript wird beendet.")
        return

    removed_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(ALLOWED_EXTENSIONS):
                if check_for_incomplete_tags(file_path):
                    # Nur wenn ein unvollständiger Tag gefunden wird, wird der Löschvorgang gestartet
                    if remove_digikam_tags(file_path):
                        removed_count += 1
                else:
                    # print(f"➡️ Keine unvollständigen Tags gefunden in: {file_path}")
                    pass  # Kommentiert, um die Konsolenausgabe zu reduzieren

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 50)
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {removed_count} Dateien bereinigt (XMP-Tags entfernt).")
    print(f"Dauer: {duration:.2f} Sekunden")
    print("=" * 50)


if __name__ == '__main__':
    main()