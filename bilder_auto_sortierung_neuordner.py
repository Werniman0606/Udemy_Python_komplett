# ==============================================================================
# Dateiname Vorschlag (Deutsch): bilder_auto_sortierung_neuordner.py
# Dateiname Vorschlag (Technisch): full_collection_sorter_creator.py
#
# Beschreibung: Dieses Skript automatisiert die Sortierung und Organisation von
#               Bilddateien aus einem Sammelordner (d:\Bilder) in eine bereits
#               existierende Prominenten-Ordnerstruktur (e:\Bilder\Celebrities\A\...).
#
#               Die Logik arbeitet in zwei Hauptprioritäten:
#               1. Priorität: Prüfen, ob der Dateiname (Best-Match-Logik) zu einem
#                  bereits EXISTIERENDEN Personenordner passt (Verschieben).
#               2. Priorität: Wenn kein Ordner passt, wird der Name aus dem
#                  Dateipräfix [Name,...]_ extrahiert (bei Kommas nur der erste Name)
#                  und ein NEUER Ordner im korrekten Initialen-Schema erstellt
#                  (z.B. Heidi Klum -> H\Heidi Klum), bevor die Datei verschoben wird.
# ==============================================================================

import os
import shutil
import re

# --- Definiere die Pfade ---
source_folder_with_celebs = r'e:\Bilder\Celebrities'
folder_with_files_to_move = r'e:\Bilder\Celebrities\B\Britta Hofmann'
# Regulärer Ausdruck, um den Namen in eckigen Klammern zu finden: \[([^\]]+)\]
# Gruppe 1 ([^\]]+) fängt den Inhalt der Klammern (z.B. "Heidi Klum, Leni Klum").
NAME_PATTERN = re.compile(r'\[([^\]]+)\]')

# --- 1. Personenordner und Namen sammeln (rekursiv) ---
print(f"Sammle vorhandene Ordner aus: {source_folder_with_celebs}\n")
celeb_folders = {}  # Speichert Name (klein) -> Pfad

for root, dirs, _ in os.walk(source_folder_with_celebs):
    for folder_name in dirs:
        full_path = os.path.join(root, folder_name)

        # Nur Ordner speichern, die NICHT die oberste Initialen-Ebene sind (z.B. A, B, C).
        # Die Bedingung root != source_folder_with_celebs prüft dies.
        if root != source_folder_with_celebs or len(folder_name) > 1:
            celeb_folders[folder_name.lower()] = full_path

# --- 2. Prominentennamen nach Länge sortieren ---
# Längere Namen zuerst, um "Annabelle" vor "Ann" zu finden (Best-Match-Logik).
sorted_celeb_names = sorted(celeb_folders.keys(), key=len, reverse=True)

print("\n------------------------------------------------\n")
print(f"Suche und organisiere Dateien in: {folder_with_files_to_move}\n")

# --- 3. Dateien durchsuchen, verschieben oder neuen Ordner erstellen ---
moved_count = 0
created_folder_count = 0

for root, _, files in os.walk(folder_with_files_to_move):
    for filename in files:
        file_path = os.path.join(root, filename)
        found_match = False

        # Ignoriere den "Chaos" Ordner, falls er im Zielpfad d:\Bilder existiert und durchsucht wird
        if os.path.basename(root).lower() == 'chaos':
            print(f"  Info: Ignoriere Datei in Chaos-Ordner: '{filename}'")
            continue

        # ERSTE PRIORITÄT: Prüfe, ob die Datei zu einem BEREITS EXISTIERENDEN Personenordner passt
        # Hier wird der gesamte Dateiname geprüft (Best-Match-Logik).
        for celeb_name_lower in sorted_celeb_names:
            # Stellt sicher, dass die Datei den Namen enthält.
            if celeb_name_lower in filename.lower():
                destination_path = celeb_folders[celeb_name_lower]
                final_destination = os.path.join(destination_path, filename)

                try:
                    shutil.move(file_path, final_destination)
                    print(f"  ✅ VERSCHOBEN (Vorhanden): '{filename}' -> '{destination_path}'")
                    moved_count += 1
                except Exception as e:
                    print(f"  ⚠️ Fehler beim Verschieben von '{filename}': {e}")

                found_match = True
                break  # Wenn der beste Match gefunden und verschoben wurde, weiter zur nächsten Datei.

        # ZWEITE PRIORITÄT: Wenn KEIN vorhandener Ordner passt, versuche, einen NEUEN zu erstellen.
        if not found_match:
            match = NAME_PATTERN.search(filename)

            if match:
                # Extrahiert den gesamten Inhalt: "Heidi Klum, Leni Klum"
                full_extracted_name = match.group(1).strip()

                # NEUE LOGIK: Prüfen auf Komma und nur den ersten Teil verwenden
                if ',' in full_extracted_name:
                    # Schneidet den Namen beim ersten Komma ab: "Heidi Klum"
                    extracted_name = full_extracted_name.split(',')[0].strip()
                    print(f"  Info: Komma gefunden. Verwende nur den ersten Namen: '{extracted_name}'")
                else:
                    extracted_name = full_extracted_name

                # Schutz vor Initialen-Ordnern (A, B, C...)
                if extracted_name.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(extracted_name) == 1:
                    print(f"  Ignoriert: '{filename}' enthält nur ein Initial als Name.")
                    continue

                # *Unwahrscheinliche* Prüfung: Prüfen, ob der Name (nach Komma-Filter) doch existiert
                if extracted_name.lower() in celeb_folders:
                    destination_path = celeb_folders[extracted_name.lower()]
                    final_destination = os.path.join(destination_path, filename)

                    # Logik fast identisch zum oberen Move-Block, nur die Meldung ist anders.
                    try:
                        shutil.move(file_path, final_destination)
                        print(f"  ✅ VERSCHOBEN (Vorhanden durch Komma-Filter): '{filename}' -> '{destination_path}'")
                        moved_count += 1
                        found_match = True
                    except Exception as e:
                        print(f"  ⚠️ Fehler beim Verschieben von '{filename}': {e}")

                # Falls der Ordner noch immer NICHT existiert, NEU ERSTELLEN
                elif extracted_name.lower() not in celeb_folders:

                    # 1. Bestimme den Anfangsbuchstaben (H)
                    first_letter = extracted_name[0].upper()

                    # 2. Erstelle den Pfad zum Zielordner (z.B. e:\Bilder\Celebrities\H\Heidi Klum)
                    new_destination_path = os.path.join(source_folder_with_celebs, first_letter, extracted_name)
                    final_destination = os.path.join(new_destination_path, filename)

                    try:
                        # Erstellt beide Ordner (H und Heidi Klum) falls sie fehlen.
                        os.makedirs(new_destination_path, exist_ok=True)
                        print(f"  ➡️ NEU: Ordner erstellt: '{new_destination_path}'")
                        created_folder_count += 1

                        # Verschiebe die Datei
                        shutil.move(file_path, final_destination)
                        print(f"  ✅ VERSCHOBEN (Neu/Komma-Filter): '{filename}' -> '{new_destination_path}'")
                        moved_count += 1
                        found_match = True

                        # Füge den neuen Ordner hinzu (wichtig für nachfolgende Dateien im selben Lauf)
                        celeb_folders[extracted_name.lower()] = new_destination_path
                        # Das Sortier-Array wird NICHT aktualisiert, da die Performance leidet.

                    except Exception as e:
                        print(f"  ⚠️ Fehler beim Erstellen/Verschieben von '{filename}' (Neu): {e}")

        # KORRIGIERTER BLOCK FÜR NICHT ZUGEORDNETE DATEIEN:
        if not found_match:
            print(f"  ❌ NICHT ZUGEORDNET: '{filename}' (Kein Match, kein erkannter Name im Muster)")

# --- 4. Abschlussbericht ---
print("\n------------------------------------------------")
print(f"✅ Vorgang abgeschlossen.")
print(f"Dateien verschoben: {moved_count}")
print(f"Neue Ordner erstellt: {created_folder_count}")
print("------------------------------------------------")