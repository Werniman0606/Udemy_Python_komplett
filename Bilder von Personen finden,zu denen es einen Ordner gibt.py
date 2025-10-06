import os
import shutil

# --- Definiere die Pfade ---
# Der Ordner, der die Personenordner enthält. os.walk durchsucht diesen rekursiv.
source_folder_with_celebs = r'e:\Bilder\Celebrities'

# Der Ordner, der die zu verschiebenden Dateien enthält. os.walk durchsucht diesen ebenfalls rekursiv.
folder_with_files_to_move = r'd:\extracted\rips'

# --- 1. Personenordner und Namen sammeln (rekursiv) ---
print(f"Sammle Namen aus allen Unterordnern in: {source_folder_with_celebs}\n")
celeb_folders = {} # Ein Dictionary, um die Namen und ihre vollständigen Pfade zu speichern.

for root, dirs, _ in os.walk(source_folder_with_celebs):
    for folder_name in dirs:
        # Ignoriere Ordner, die nur aus einem einzigen Buchstaben bestehen.
        if len(folder_name) > 1:
            full_path = os.path.join(root, folder_name)
            celeb_folders[folder_name.lower()] = full_path
            print(f"  Gefundener Prominenter: '{folder_name}' -> '{full_path}'")

if not celeb_folders:
    print("\nEs wurden keine Personenordner gefunden (oder nur einzelne Buchstaben). Skript wird beendet.")
    exit()

# --- 2. Prominentennamen nach Länge sortieren, um längere Namen zuerst zu finden ---
# Dies stellt sicher, dass "Heidi Klum" vor "Heidi" gefunden wird.
sorted_celeb_names = sorted(celeb_folders.keys(), key=len, reverse=True)

print("\n------------------------------------------------\n")
print(f"Suche nach Dateien in: {folder_with_files_to_move}\n")

# --- 3. Dateien durchsuchen und verschieben (rekursiv) ---
moved_count = 0 # Zähler für die verschobenen Dateien.

for root, _, files in os.walk(folder_with_files_to_move):
    for filename in files:
        file_path = os.path.join(root, filename)

        found_match = False
        # Überprüfe jeden Prominentennamen gegen den Dateinamen.
        # Die Liste ist jetzt nach Namenlänge sortiert (lange Namen zuerst).
        for celeb_name_lower in sorted_celeb_names:
            # Prüfe, ob der Dateiname den Prominentennamen (in Kleinbuchstaben) enthält.
            if celeb_name_lower in filename.lower():
                # Finde den vollständigen Pfad zum Ordner.
                destination_path = celeb_folders[celeb_name_lower]
                final_destination = os.path.join(destination_path, filename)

                try:
                    shutil.move(file_path, final_destination)
                    print(f"  Verschoben: '{filename}' -> '{final_destination}'")
                    moved_count += 1
                except Exception as e:
                    print(f"  Fehler beim Verschieben von '{filename}': {e}")

                found_match = True
                # Nachdem die Datei verschoben wurde, brechen wir die innere Schleife ab.
                break

        if not found_match:
            print(f"  Keine Übereinstimmung für '{filename}' gefunden.")

print("\n------------------------------------------------\n")
print(f"Vorgang abgeschlossen. {moved_count} Dateien wurden verschoben.")