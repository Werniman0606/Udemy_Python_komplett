# ==============================================================================
# Dateiname: rename_images_with_model_name.py
# Beschreibung: Extrahiert den Modellnamen aus dem Format "ID-Name-ID.ext"
#                und setzt ihn als [Name]_ Präfix vor den Dateinamen.
#
# Funktioniert nativ unter Windows UND Linux (CachyOS).
# ==============================================================================

import os
import re
from pathlib import Path

# --- KONFIGURATION & BETRIEBSSYSTEM-ERKENNUNG ---
if os.name == 'nt':  # Windows
    DIRECTORY = Path(r'd:\extracted\rips')
else:  # Linux (CachyOS)
    DIRECTORY = Path("/run/media/marcoj/Laufwerk D/extracted/rips")

FILE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')


def rename_images_with_model_name():
    # Prüfen, ob das Verzeichnis existiert
    if not DIRECTORY.is_dir():
        print(f"Fehler: Das Verzeichnis {DIRECTORY} wurde nicht gefunden.")
        return

    count = 0

    # 1. Alle passenden Bilddateien der ersten Ebene VORAB einlesen,
    # um zu verhindern, dass bereits umbenannte Dateien doppelt verarbeitet werden.
    files_to_process = [
        f for f in DIRECTORY.iterdir()
        if f.is_file() and f.suffix.lower() in FILE_EXTENSIONS
    ]

    print(f"Starte Verarbeitung in: {DIRECTORY}")
    print("-" * 60)

    for file_path in files_to_process:
        filename = file_path.name

        # Sicherheitsprüfung: Hat die Datei bereits ein eckiges Präfix? (z.B. durch abgebrochenen Vorlauf)
        if re.match(r'^\[.+?\]_', filename):
            print(f"Übersprungen (bereits ein Präfix vorhanden): {filename}")
            continue

        try:
            # Trennung am Bindestrich (Format: "ID-Name-ID.ext")
            parts = filename.split('-')

            # Sicherstellen, dass mindestens zwei Bindestriche vorhanden sind
            if len(parts) >= 3:
                model_name = parts[1].strip()
                new_filename = f"[{model_name}]_{filename}"

                # Pfad plattformunabhängig mit dem / Operator zusammensetzen
                new_file_path = DIRECTORY / new_filename

                # Umbenennung durchführen
                file_path.rename(new_file_path)
                count += 1
                print(f"✅ Umbenannt: {filename} -> {new_filename}")
            else:
                print(f"⚠️ Übersprungen (falsches Format): {filename}")

        except Exception as e:
            print(f"❌ Fehler bei Datei {filename}: {e}")

    print("-" * 60)
    print(f"Fertig! Es wurden {count} Dateien erfolgreich umbenannt.")


if __name__ == "__main__":
    rename_images_with_model_name()