# ==============================================================================
# Dateiname Vorschlag (Deutsch): bilder_tag_qualitaet_sortierer.py
# Dateiname Vorschlag (Technisch): exiftool_region_creator_sorter.py
#
# Beschreibung: Dieses Skript dient der Qualitätssicherung und Organisation von
#               getaggten Bildern. Es durchsucht ein Quellverzeichnis (SOURCE_DIR)
#               und verschiebt eine Datei nur dann in das Zielverzeichnis (DEST_DIR),
#               wenn die Anzahl der gefundenen Gesichtsregionen (Regions) exakt
#               der Anzahl der Personennamen im XMP-dc:creator-Tag entspricht.
#               Dies stellt sicher, dass nur "vollständig" getaggte Bilder
#               organisiert werden, während ungetaggte oder unvollständig
#               getaggte Bilder im Quellordner verbleiben.
# ==============================================================================

import os
import subprocess
import shutil
import time

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder\Celebrities\C\Chloe Morgane'

# Zielverzeichnis für getaggte Dateien
DEST_DIR = r'e:\Bilder-getaggt\Celebrities\C\Chloe Morgane'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


# --- KONFIGURATION ENDE ---

def get_tag_counts(file_path):
    """
    Zählt die Anzahl der Gesichtsregionen (Regions) und der Personennamen (Creator)
    mithilfe verschiedener gängiger XMP-Tags, um einen robusten Vergleich zu ermöglichen.
    """
    try:
        # Fragt nach verschiedenen Region-Tags (MWG, ACDSee) und dem Creator-Tag.
        # -T sorgt für Tabulator-getrennte Ausgabe.
        command = f'chcp 65001 & "{EXIFTOOL_PATH}" -T -XMP:RegionList -MP:RegionList -XMP-mwg-rs:Regions -XMP-acdsee-rs:ACDSeeRegionName -XMP-dc:creator "{file_path}"'

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

        # Die erwarteten Felder (Index 0 bis 4) müssen in der Ausgabe vorhanden sein
        if len(output_list) < 5:
            return 0, 0

        region_count = 0
        creator_count = 0

        # Annahme der Spalten basierend auf dem ExifTool-Befehl:
        # [0] = RegionList, [1] = MP:RegionList, [2] = MWG-Regions, [3] = ACDSeeRegionName, [4] = Creator

        regions_output_mwg = output_list[2]
        regions_output_acdsee = output_list[3]
        creators_output = output_list[4]

        # Zählung der Regionen (MWG-Regions verwendet meist geschweifte Klammern {})
        if regions_output_mwg and regions_output_mwg != '-':
            region_count = regions_output_mwg.count('{')

        # Zählung der Regionen (ACDSeeRegionName verwendet meist Kommas)
        elif regions_output_acdsee and regions_output_acdsee != '-':
            # Wenn kein Komma, aber ein Eintrag existiert, ist es 1 Tag
            region_count = regions_output_acdsee.count(',') + 1

        # Zählung der Creator-Tags (verwendet Kommas, wenn mehrere Tags existieren)
        if creators_output and creators_output != '-':
            # Wenn kein Komma, aber ein Eintrag existiert, ist es 1 Tag
            creator_count = creators_output.count(',') + 1

        return region_count, creator_count

    except Exception as e:
        print(f"⚠️ Fehler beim Lesen von Tags für {file_path}: {e}")
        return 0, 0


def move_file(source_path, dest_base_dir):
    """
    Verschiebt eine Datei und behält dabei die ursprüngliche Verzeichnisstruktur bei.
    """
    # Bestimme den relativen Pfad relativ zum Quellordner
    relative_path = os.path.relpath(source_path, SOURCE_DIR)
    # Erstelle den vollen Zielpfad
    dest_path = os.path.join(dest_base_dir, relative_path)
    # Stelle sicher, dass der Zielordner existiert
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        # Verschiebt die Datei
        shutil.move(source_path, dest_path)
        return True
    except Exception as e:
        print(f"❌ Fehler beim Verschieben von '{os.path.basename(source_path)}': {e}")
        return False


def main():
    print("Starte den Verschiebe-Vorgang für qualitätsgeprüfte, getaggte Bilder...")
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

                # Hauptkriterium: Es muss mindestens 1 Tag existieren UND die Anzahl der Regionen
                # muss mit der Anzahl der Creator-Namen übereinstimmen.
                if creator_count > 0 and region_count == creator_count:
                    if move_file(file_path, DEST_DIR):
                        print(
                            f"✅ Verschiebe: {os.path.basename(file_path)} (Tags: {creator_count} / Regionen: {region_count})")
                        moved_count += 1
                else:
                    # print(f"➡️ Überspringe: {os.path.basename(file_path)} (Tags: {creator_count} / Regionen: {region_count})")
                    pass  # Überspringt die Datei, wenn die Tag-Qualität nicht stimmt

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 50)
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {moved_count} Dateien verschoben (als qualifiziert getaggt).")
    print(f"Dauer: {duration:.2f} Sekunden")
    print("=" * 50)


if __name__ == '__main__':
    main()