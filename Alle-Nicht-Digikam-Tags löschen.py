import os
import subprocess
import time
import re

# --- KONFIGURATION START ---
# Pfad zu exiftool.exe
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'e:\Bilder\Celebrities\C\Chloe Morgane'

# Erlaubte Namespaces (Gruppen), die BEHALTEN werden sollen.
# Füge den Doppelpunkt am Ende hinzu, damit ExifTool es korrekt erkennt.
ALLOWED_TAGS = [
    'XMP-digiKam:',
    'XMP-mwg-rs:',
]

# Erlaubte Dateiendungen
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.gif')

# --- KONFIGURATION ENDE ---

def get_xmp_namespaces(file_path):
    """
    Liest alle XMP-Namespaces einer Datei aus.
    Gibt eine Liste von Namensräumen zurück, z.B. ['XMP-photoshop:', 'XMP-digiKam:'].
    """
    command = [EXIFTOOL_PATH, '-xmp:all', '-s', '-s', '-G1', file_path]
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            encoding='utf-8',
            errors='ignore'
        )
        namespaces = set()
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                # Extrahiert den Namespace aus der Ausgabe "[NAMESPACE]TAG"
                match = re.search(r'\[(XMP-\w+):\]', line)
                if match:
                    namespaces.add(match.group(1) + ':')
        return list(namespaces)
    except Exception as e:
        print(f"⚠️ Fehler beim Auslesen von Namespaces für {file_path}: {e}")
        return []

def remove_unwanted_tags(file_path):
    """
    Entfernt alle XMP-Tags, die nicht in der ALLOWED_TAGS-Liste sind.
    """
    print(f"\n🔄 Verarbeite {os.path.basename(file_path)}...")

    current_namespaces = get_xmp_namespaces(file_path)
    print(f"DEBUG: Gefundene XMP-Namespaces in der Datei: {current_namespaces}")

    tags_to_delete = []
    for namespace in current_namespaces:
        if namespace not in ALLOWED_TAGS:
            tags_to_delete.append(f'-{namespace}all')

    if not tags_to_delete:
        print(f"✅ Keine unerwünschten XMP-Tags zum Entfernen gefunden.")
        return False

    # NEUER Befehl: -overwrite_original_in_place
    command = [EXIFTOOL_PATH] + tags_to_delete + ['-overwrite_original_in_place', file_path]
    print(f"DEBUG: Löschbefehl: {command}")

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            encoding='utf-8',
            errors='ignore'
        )

        if result.returncode == 0 and "1 image files updated" in result.stdout:
            print(f"✅ Unerwünschte XMP-Tags erfolgreich entfernt.")
            return True
        else:
            print(f"❌ Fehler beim Entfernen der Tags: {result.stderr}")
            return False

    except Exception as e:
        print(f"⚠️ Ausnahmefehler: {e}")
        return False

def main():
    print("Starte den Vorgang zum selektiven Entfernen von Tags...")
    print(f"Suche nach Bildern in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Fehler: Quellverzeichnis '{SOURCE_DIR}' nicht gefunden.")
        return

    processed_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(ALLOWED_EXTENSIONS):
                if remove_unwanted_tags(file_path):
                    processed_count += 1

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {processed_count} Dateien bereinigt.")
    print(f"Dauer: {duration:.2f} Sekunden")

if __name__ == '__main__':
    main()