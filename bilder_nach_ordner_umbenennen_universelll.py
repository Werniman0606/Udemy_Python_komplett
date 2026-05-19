# ==============================================================================
# Dateiname: rename_prefix_with_folder.py
#
# Beschreibung: Dieses Skript durchläuft rekursiv (inklusive Unterordnern)
#                alle Bilddateien ab einem Basispfad. Es benennt jede Bilddatei
#                um, indem es den Namen ihres direkten Elternordners in eckigen
#                Klammern als Präfix vor den ursprünglichen Dateinamen setzt.
#                (Beispiel: 1.jpg in Ordner "Stars" wird zu [Stars]_1.jpg).
#                Bereits getaggte Dateien werden übersprungen.
#
# Funktioniert nativ unter Windows UND Linux (CachyOS).
# ==============================================================================

import os
from pathlib import Path

# --- KONFIGURATION & BETRIEBSSYSTEM-ERKENNUNG ---
if os.name == 'nt':  # Windows
    BASE_DIRECTORY = Path(r'd:\extracted\rips\reddit_sub_GermanCelebs')
else:  # Linux (CachyOS)
    BASE_DIRECTORY = Path("/run/media/marcoj/Laufwerk D/extracted/rips/reddit_sub_GermanCelebs")

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.avif')


def rename_images_with_folder_name(base_path):
    """
    Benennt Bilddateien in einem Verzeichnis und allen Unterverzeichnissen um.
    Fügt den Namen des Elternordners als [Ordnername]_ Präfix hinzu.
    """
    if not base_path.is_dir():
        print(f"Fehler: Der Basispfad '{base_path}' existiert nicht oder ist kein Verzeichnis.")
        return

    print(f"Starte Umbenennungsvorgang im Basispfad: {base_path}")
    print("-" * 70)

    # 1. Alle Dateien vorab sammeln (Snapshot), um Schleifenfehler beim Umbenennen zu vermeiden
    print("Analysiere Ordnerstruktur...")
    files_to_process = [
        f for f in base_path.rglob('*')
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]
    print(f"-> {len(files_to_process)} Bilddateien zur Verarbeitung gefunden.\n")

    for file_path in files_to_process:
        filename = file_path.name

        # Wenn der Dateiname bereits mit einer öffnenden eckigen Klammer beginnt, überspringen
        if filename.startswith('['):
            print(f"  Überspringe '{filename}' (bereits getaggt oder umbenannt).")
            continue

        # Der Name des direkten Elternordners ist genial einfach über .parent.name erreichbar
        parent_folder_name = file_path.parent.name

        # Konstruiere den neuen Dateinamen
        # .name enthält den vollen Namen inklusive Endung
        new_filename = f"[{parent_folder_name}]_{filename}"
        new_file_path = file_path.parent / new_filename

        try:
            # Umbenennung durchführen
            file_path.rename(new_file_path)
            print(f"  ✅ Umbenannt: '{filename}' -> '{new_filename}'")
        except OSError as e:
            print(f"  ❌ Fehler beim Umbenennen von '{filename}': {e}")

    print("-" * 70)
    print("Umbenennungsvorgang abgeschlossen.")


if __name__ == "__main__":
    # Ein vollständiges Backup der Dateien wird vor dem Ausführen weiterhin empfohlen.
    rename_images_with_folder_name(BASE_DIRECTORY)