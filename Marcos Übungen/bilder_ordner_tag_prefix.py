# ==============================================================================
# Dateiname Vorschlag (Deutsch): bilder_ordner_tag_prefix.py
# Dateiname Vorschlag (Technisch): rename_prefix_if_missing.py
#
# Beschreibung: Dieses Skript durchläuft alle Unterordner ab einem Basispfad
#               (SOURCE_DIR) und versieht die Bilddateien in diesen Ordnern mit
#               einem Präfix. Das Präfix ist der Name des jeweiligen
#               Elternordners in eckigen Klammern, gefolgt von einem Unterstrich
#               (z.B. [Beatrice Egli]_). Dateien, die bereits ein beliebiges
#               Präfix im Format '[...]_' besitzen, werden übersprungen, um
#               Doppeltagging oder Konflikte zu vermeiden.
# ==============================================================================

import os
import time
import re # Importiere das Modul für reguläre Ausdrücke

# --- CONFIGURATION START ---
# Source directory where the script will start looking for files
SOURCE_DIR = r'd:\RedditDownloads\reddit_sub_GermanCelebs'

# Allowed image formats
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')

# Regulärer Ausdruck, der ein Präfix in der Form "[...]_" matcht.
# Das Muster sucht nach: [ (beliebige Zeichen) ] _
# Die Zeichen '[]' müssen mit dem Backslash escaped werden, da sie Sonderzeichen sind.
PRE_EXISTING_PREFIX_PATTERN = r'^\[.*?\]_'

# --- CONFIGURATION END ---

def main():
    print("Starting the file renaming process...")
    print(f"Searching for images in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Error: Source directory '{SOURCE_DIR}' not found.")
        return

    renamed_count = 0
    start_time = time.time()

    # Walk through the source directory and its subdirectories
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Exclude the base directory itself (da das Basis-Verzeichnis i.d.R. keinen Namen hat)
        if root == SOURCE_DIR:
            continue

        # Get the name of the current folder, e.g., "Beatrice Egli"
        folder_name = os.path.basename(root)

        # Das benötigte Präfix in der gewünschten Form, z.B. "[Beatrice Egli]_"
        required_prefix = f'[{folder_name}]_'

        for file in files:
            # Check if the file is an allowed image format
            if file.lower().endswith(ALLOWED_EXTENSIONS):

                # Prüfe mit Regex, ob ein beliebiges Namens-Präfix in eckigen Klammern vorhanden ist
                if re.match(PRE_EXISTING_PREFIX_PATTERN, file):
                    print(f"➡️ Skipping: '{file}' (Prefix '[...]_' already exists from another script)")
                    continue  # Springe zur nächsten Datei, da die Datei bereits "getaggt" ist

                # Wenn keine eckigen Klammern vorhanden sind, wird normal umbenannt:
                file_path = os.path.join(root, file)

                # Create the new file name
                new_file_name = f'{required_prefix}{file}'
                new_file_path = os.path.join(root, new_file_name)

                try:
                    os.rename(file_path, new_file_path)
                    print(f"✅ Renamed: '{file}' -> '{new_file_name}'")
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ Error renaming '{file}': {e}")
            else:
                print(f"➡️ Skipping non-image file: '{file}'")

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 50)
    print("Process complete.")
    print(f"Total {renamed_count} files renamed.")
    print(f"Duration: {duration:.2f} seconds")
    print("=" * 50)


if __name__ == '__main__':
    main()