# ==============================================================================
# Dateiname Vorschlag (Deutsch): bilder_auto_sortierung_neuordner.py
# Dateiname Vorschlag (Technisch): full_collection_sorter_creator.py
#
# Beschreibung: Dieses Skript automatisiert die Sortierung und Organisation von
#                Bilddateien aus einem Sammelordner in eine bereits
#                existierende Prominenten-Ordnerstruktur.
#
#                Funktioniert nativ unter Windows UND Linux (CachyOS).
# ==============================================================================

import os
import shutil
import re
from pathlib import Path

# --- Automatische Betriebssystem-Erkennung & Pfad-Zuweisung ---
if os.name == 'nt':  # Windows
    SOURCE_CELEBS_BASE = Path(r"E:\Bilder\Celebrities")
    FOLDER_TO_MOVE_BASE = Path(r"D:\extracted\rips")
else:  # Linux (CachyOS)
    SOURCE_CELEBS_BASE = Path("/run/media/marcoj/Laufwerk E/Bilder/Celebrities")
    FOLDER_TO_MOVE_BASE = Path("/run/media/marcoj/Laufwerk D/extracted/rips")

# Regulärer Ausdruck, um den Namen in eckigen Klammern zu finden: \[([^\]]+)\]
NAME_PATTERN = re.compile(r'\[([^\]]+)\]')

# --- 1. Personenordner und Namen sammeln (rekursiv) ---
print(f"Sammle vorhandene Ordner aus: {SOURCE_CELEBS_BASE}\n")
celeb_folders = {}  # Speichert Name (klein) -> Path-Objekt

# os.walk akzeptiert Path-Objekte, wir konvertieren root zur Weiterverarbeitung in Path
for root_str, dirs, _ in os.walk(SOURCE_CELEBS_BASE):
    root = Path(root_str)
    for folder_name in dirs:
        full_path = root / folder_name

        # Nur Ordner speichern, die NICHT die oberste Initialen-Ebene sind (z.B. A, B, C).
        if root != SOURCE_CELEBS_BASE or len(folder_name) > 1:
            celeb_folders[folder_name.lower()] = full_path

# --- 2. Prominentennamen nach Länge sortieren ---
sorted_celeb_names = sorted(celeb_folders.keys(), key=len, reverse=True)

print("\n------------------------------------------------\n")
print(f"Suche und organisiere Dateien in: {FOLDER_TO_MOVE_BASE}\n")

# --- 3. Dateien durchsuchen, verschieben oder neuen Ordner erstellen ---
moved_count = 0
created_folder_count = 0

for root_str, _, files in os.walk(FOLDER_TO_MOVE_BASE):
    root = Path(root_str)
    for filename in files:
        file_path = root / filename
        found_match = False

        # Ignoriere den "Chaos" Ordner, falls er im Zielpfad existiert
        if root.name.lower() == 'chaos':
            print(f"   Info: Ignoriere Datei in Chaos-Ordner: '{filename}'")
            continue

        # ERSTE PRIORITÄT: Prüfe, ob die Datei zu einem BEREITS EXISTIERENDEN Personenordner passt
        filename_lower = filename.lower()
        for celeb_name_lower in sorted_celeb_names:
            if celeb_name_lower in filename_lower:
                destination_path = celeb_folders[celeb_name_lower]
                final_destination = destination_path / filename

                try:
                    shutil.move(file_path, final_destination)
                    print(f"   ✅ VERSCHOBEN (Vorhanden): '{filename}' -> '{destination_path}'")
                    moved_count += 1
                except Exception as e:
                    print(f"   ⚠️ Fehler beim Verschieben von '{filename}': {e}")

                found_match = True
                break  # Best-Match gefunden -> Nächste Datei

        # ZWEITE PRIORITÄT: Wenn KEIN vorhandener Ordner passt, versuche, einen NEUEN zu erstellen.
        if not found_match:
            match = NAME_PATTERN.search(filename)

            if match:
                full_extracted_name = match.group(1).strip()

                # NEUE LOGIK: Prüfen auf Komma und nur den ersten Teil verwenden
                if ',' in full_extracted_name:
                    extracted_name = full_extracted_name.split(',')[0].strip()
                    print(f"   Info: Komma gefunden. Verwende nur den ersten Namen: '{extracted_name}'")
                else:
                    extracted_name = full_extracted_name

                # Schutz vor Initialen-Ordnern (A, B, C...)
                if extracted_name.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(extracted_name) == 1:
                    print(f"   Ignoriert: '{filename}' enthält nur ein Initial als Name.")
                    continue

                extracted_name_lower = extracted_name.lower()

                # Prüfen, ob der Name (nach Komma-Filter) doch existiert
                if extracted_name_lower in celeb_folders:
                    destination_path = celeb_folders[extracted_name_lower]
                    final_destination = destination_path / filename

                    try:
                        shutil.move(file_path, final_destination)
                        print(f"   ✅ VERSCHOBEN (Vorhanden durch Komma-Filter): '{filename}' -> '{destination_path}'")
                        moved_count += 1
                        found_match = True
                    except Exception as e:
                        print(f"   ⚠️ Fehler beim Verschieben von '{filename}': {e}")

                # Falls der Ordner noch immer NICHT existiert, NEU ERSTELLEN
                else:
                    first_letter = extracted_name[0].upper()

                    # Pfad dynamisch zusammenbauen
                    new_destination_path = SOURCE_CELEBS_BASE / first_letter / extracted_name
                    final_destination = new_destination_path / filename

                    try:
                        # Erstellt Ordnerstruktur falls sie fehlt (exist_ok=True verhindert Fehler)
                        new_destination_path.mkdir(parents=True, exist_ok=True)
                        print(f"   ➡️ NEU: Ordner erstellt: '{new_destination_path}'")
                        created_folder_count += 1

                        # Verschiebe die Datei
                        shutil.move(file_path, final_destination)
                        print(f"   ✅ VERSCHOBEN (Neu/Komma-Filter): '{filename}' -> '{new_destination_path}'")
                        moved_count += 1
                        found_match = True

                        # Füge den neuen Ordner zur Laufzeit-Liste hinzu
                        celeb_folders[extracted_name_lower] = new_destination_path

                    except Exception as e:
                        print(f"   ⚠️ Fehler beim Erstellen/Verschieben von '{filename}' (Neu): {e}")

        # KORRIGIERTER BLOCK FÜR NICHT ZUGEORDNETE DATEIEN:
        if not found_match:
            print(f"   ❌ NICHT ZUGEORDNET: '{filename}' (Kein Match, kein erkannter Name im Muster)")

# --- 4. Abschlussbericht ---
print("\n------------------------------------------------")
print(f"✅ Vorgang abgeschlossen.")
print(f"Dateien verschoben: {moved_count}")
print(f"Neue Ordner erstellt: {created_folder_count}")
print("------------------------------------------------")