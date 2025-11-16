# ==============================================================================
# Dateiname Vorschlag (Deutsch): bilder_nach_face_tagging_verschieben.py
# Dateiname Vorschlag (Technisch): exiftool_face_tag_sorter.py
#
# Beschreibung: Dieses Skript durchsucht rekursiv ein Quellverzeichnis (SOURCE_DIR)
#               nach allen Bildern. Es ruft ExifTool auf, um zu prüfen, ob die
#               Datei Metadaten für getaggte Gesichtsregionen/Personen enthält
#               (XMP-MP:RegionPersonDisplayName und RegionPersonRegion).
#               Dateien, die mindestens einen vollständigen Personen-Tag aufweisen,
#               werden unter Beibehaltung ihrer relativen Ordnerstruktur in den
#               Zielordner (DEST_DIR) verschoben.
# ==============================================================================

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
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.gif')


# --- KONFIGURATION ENDE ---

def get_tag_counts(file_path):
    """
    Zählt die Anzahl der Gesichtsregionen und getaggten Personen, indem
    explizit nach beiden notwendigen XMP-Tags gesucht wird (Digikam/Adobe Standard).

    Gibt (Anzahl der Regionen, Anzahl der Personen-Tags) zurück.
    """
    try:
        # Fragen Sie explizit nach beiden Tags im Tabulator-getrennten Format (-T).
        # chcp 65001 stellt sicher, dass die Konsole UTF-8 korrekt verarbeitet.
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

        # Die Ausgabe sollte aus zwei Feldern bestehen (Name und Region)
        if len(output_list) == 2:
            display_names_str = output_list[0].strip()
            regions_str = output_list[1].strip()

            # Prüfe, ob beide Tags nicht nur ein einfaches Trennzeichen ('-') sind
            if display_names_str != '-' and regions_str != '-':
                # Die Anzahl der Tags ist die Anzahl der Kommas + 1
                name_count = display_names_str.count(',') + 1 if ',' in display_names_str else (
                    1 if display_names_str else 0)
                region_count = regions_str.count(',') + 1 if ',' in regions_str else (1 if regions_str else 0)

                # Die Anzahl der Namen muss mit der Anzahl der Regionen übereinstimmen
                if name_count > 0 and name_count == region_count:
                    return name_count, name_count

        return 0, 0

    except Exception as e:
        print(f"⚠️ Fehler beim Lesen von Tags für {file_path}: {e}")
        return 0, 0


def move_file(source_path, dest_base_dir):
    """
    Verschiebt eine Datei und behält dabei die ursprüngliche Verzeichnisstruktur bei.
    """
    # Bestimme den relativen Pfad (z.B. 'Urlaub\2024\bild.jpg')
    relative_path = os.path.relpath(source_path, SOURCE_DIR)
    # Erstelle den vollen Zielpfad (z.B. 'e:\Bilder-getaggt\Urlaub\2024\bild.jpg')
    dest_path = os.path.join(dest_base_dir, relative_path)
    # Stelle sicher, dass der Zielordner existiert
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        shutil.move(source_path, dest_path)
        return True
    except Exception as e:
        print(f"❌ Fehler beim Verschieben von '{os.path.basename(source_path)}': {e}")
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

    # Sicherheitsprüfung für Exiftool
    if not os.path.isfile(EXIFTOOL_PATH):
        print(f"❌ Fehler: Exiftool-Pfad '{EXIFTOOL_PATH}' ist ungültig. Skript wird beendet.")
        return

    moved_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)

            if file.lower().endswith(ALLOWED_EXTENSIONS):
                region_count, creator_count = get_tag_counts(file_path)

                # Die Bedingung: Es muss mindestens ein vollständiger Personen-Tag existieren.
                if creator_count > 0:
                    if move_file(file_path, DEST_DIR):
                        print(
                            f"✅ Verschiebe: {os.path.basename(file_path)} (Tags: {creator_count})")
                        moved_count += 1
                else:
                    # Optional: Ausgabe für übersprungene Dateien, um den Fortschritt zu sehen
                    # print(f"➡️ Überspringe: {os.path.basename(file_path)}")
                    pass  # Überspringt die Datei, wenn keine Tags gefunden wurden

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 50)
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {moved_count} Dateien verschoben.")
    print(f"Dauer: {duration:.2f} Sekunden")
    print("=" * 50)


if __name__ == '__main__':
    main()