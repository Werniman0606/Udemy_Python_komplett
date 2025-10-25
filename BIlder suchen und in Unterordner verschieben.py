import os
import shutil

# --- Definiere die Pfade ---
# Der Ordner, der die Personenordner enthält. os.walk durchsucht diesen rekursiv.
source_folder_with_celebs = r'e:\Celebrities'

# Der Ordner, der die zu verschiebenden Dateien enthält. os.walk durchsucht diesen ebenfalls rekursiv.
folder_with_files_to_move = r'd:\RedditDownloads\reddit_sub_GermanCelebs'

# --- 1. Personenordner und Namen sammeln (rekursiv) ---
print(f"Sammle Namen aus allen Unterordnern in: {source_folder_with_celebs}\n")
celeb_folders = {}  # Ein Dictionary, um die Namen und ihre vollständigen Pfade zu speichern.

for root, dirs, _ in os.walk(source_folder_with_celebs):
    for folder_name in dirs:
        # Ignoriere Ordner, die nur aus einem einzigen Buchstaben bestehen.
        if len(folder_name) > 1:
            full_path = os.path.join(root, folder_name)
            # Speichere den Namen in Kleinbuchstaben als Schlüssel
            celeb_folders[folder_name.lower()] = full_path
            print(f"  Gefundener Prominenter: '{folder_name}' -> '{full_path}'")

if not celeb_folders:
    print("\nEs wurden keine Personenordner gefunden (oder nur einzelne Buchstaben). Skript wird beendet.")
    exit()

# HINWEIS: sorted_celeb_names wird NICHT mehr für die Dateinamen-Suche verwendet,
# da wir nun explizit nach dem längsten Treffer suchen (siehe unten).
# Wir behalten es nur für den Fall, dass es später benötigt wird.
# sorted_celeb_names = sorted(celeb_folders.keys(), key=len, reverse=True)

print("\n------------------------------------------------\n")
print(f"Suche nach Dateien in: {folder_with_files_to_move}\n")

# --- 3. Dateien durchsuchen und verschieben (rekursiv) ---
moved_count = 0  # Zähler für die verschobenen Dateien.

for root, _, files in os.walk(folder_with_files_to_move):
    # Der Name des Ordners, der die aktuellen Dateien enthält.
    # Wir nehmen den letzten Teil des Pfades.
    current_source_folder_name = os.path.basename(root).lower()

    for filename in files:
        file_path = os.path.join(root, filename)

        # ------------------------------------------------------------------
        # Vorgehensweise:
        # 1. Höchste Priorität: Suche im aktuellen Quellordnernamen (current_source_folder_name)
        # 2. Zweite Priorität: Suche im Dateinamen (mit Best-Match-Logik)
        # ------------------------------------------------------------------

        found_match = False
        destination_path = None

        # A) Priorität 1: Suche im Quellordnernamen (Root)
        # Suche nach der ersten Übereinstimmung im aktuellen Quellordnernamen.
        for celeb_name_lower in celeb_folders.keys():
            # Prüfe, ob der Prominentenname im Quellordnernamen enthalten ist.
            if celeb_name_lower in current_source_folder_name:
                # Treffer im Quellordner hat höchste Priorität!
                destination_path = celeb_folders[celeb_name_lower]
                print(
                    f"  ✅ TREFFER im Quellordner-Namen ('{current_source_folder_name}'): '{filename}' soll zu '{os.path.basename(destination_path)}'")
                found_match = True
                break  # Gefunden, höchste Priorität erfüllt, innere Schleife abbrechen

        # B) Priorität 2: Suche im Dateinamen (Best-Match-Logik)
        if not found_match:
            best_match_name = None
            best_match_length = 0

            # Durchsuche ALLE Prominenten, um den LÄNGSTEN Namen zu finden, der passt.
            for celeb_name_lower in celeb_folders.keys():
                # Prüfe, ob der Dateiname den Prominentennamen (in Kleinbuchstaben) enthält.
                if celeb_name_lower in filename.lower():
                    # Wähle den längsten Namen, der gefunden wurde.
                    if len(celeb_name_lower) > best_match_length:
                        best_match_length = len(celeb_name_lower)
                        best_match_name = celeb_name_lower

            if best_match_name:
                # Wir haben den längsten Treffer gefunden und speichern seinen Pfad.
                destination_path = celeb_folders[best_match_name]
                print(
                    f"  ➡️ LÄNGSTER TREFFER im Dateinamen: '{filename}' soll zu '{os.path.basename(destination_path)}'")
                found_match = True

        # C) Datei verschieben oder keine Übereinstimmung melden
        if found_match and destination_path:
            final_destination = os.path.join(destination_path, filename)

            try:
                # Stelle sicher, dass wir nicht versuchen, die Datei in ihren eigenen Ordner zu verschieben
                if os.path.dirname(file_path) == destination_path:
                    print(f"  Skippe: '{filename}' ist bereits im Zielordner ('{os.path.basename(destination_path)}').")
                    continue

                shutil.move(file_path, final_destination)
                print(f"  🎉 VERSCHOBEN: '{filename}' -> '{final_destination}'")
                moved_count += 1
            except Exception as e:
                print(f"  ⚠️ Fehler beim Verschieben von '{filename}': {e}")

        elif not found_match:
            print(f"  ❌ Keine Übereinstimmung für '{filename}' gefunden.")

print("\n------------------------------------------------\n")
print(f"Vorgang abgeschlossen. {moved_count} Dateien wurden verschoben.")