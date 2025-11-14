# ==============================================================================
# Dateiname Vorschlag (Deutsch): bilder_nach_klammer_sortieren.py
# Dateiname Vorschlag (Technisch): bracket_name_folder_creator.py
#
# Beschreibung: Dieses Skript dient der automatischen Sortierung von Dateien.
#               Es extrahiert einen Namen, der in eckigen Klammern [...] im
#               Dateinamen enthalten ist, und verschiebt die Datei in eine
#               neue Zielstruktur:
#               BASISORDNER / ERSTER_BUCHSTABE / VOLLER_NAME
#
#               Beispiel: "[Jasmin Schwiers]_bild.jpg" ->
#               e:\Bilder\Celebrities\J\Jasmin Schwiers\bild.jpg
#
#               Die Unterordner werden bei Bedarf automatisch angelegt.
# ==============================================================================

import os
import shutil
import re

# --- Definiere die Pfade ---
# Dies ist der Basis-Zielordner (e:\Bilder\Celebrities)
base_destination_folder = r'e:\Bilder\Celebrities'

# Der Ordner, der die zu verschiebenden Dateien enthält. os.walk durchsucht diesen rekursiv.
folder_with_files_to_move = r'd:\rips\reddit_sub_VintageBabes'

# Regulärer Ausdruck (Compiled Pattern), um den Namen in eckigen Klammern zu finden
# Sucht nach '[...]' und erfasst den Inhalt der Klammern als Gruppe 1 (celeb_name)
NAME_PATTERN = re.compile(r'\[(.*?)\]')

print(f"Starte Sortierung: Zielordner-Basis ist '{base_destination_folder}'\n")
print(f"Suche nach Dateien in: {folder_with_files_to_move}\n")

# --- 1. Dateien durchsuchen und verschieben (rekursiv) ---
moved_count = 0  # Zähler für die verschobenen Dateien.
unmatched_count = 0  # Zähler für Dateien ohne Klammer-Namen.

for root, _, files in os.walk(folder_with_files_to_move):
    for filename in files:
        file_path = os.path.join(root, filename)

        # 1. Name aus eckigen Klammern extrahieren
        match = NAME_PATTERN.search(filename)

        if match:
            # Der Prominentenname ist der Inhalt der Klammern (Gruppe 1)
            celeb_name = match.group(1).strip()

            # Prüfen, ob der extrahierte Name nicht leer ist
            if celeb_name:

                # Bestimme den ersten Buchstaben (für den A/B/C-Ordner)
                # Konvertiere in Großbuchstaben, um die Ordner A, B, C... zu erzeugen
                first_letter = celeb_name[0].upper()

                # Überspringe Dateien, deren Name nicht mit einem Buchstaben beginnt
                if not first_letter.isalpha():
                    print(
                        f"  ⚠️ Ignoriert: Name '{celeb_name}' beginnt nicht mit einem Buchstaben. Datei: '{filename}'")
                    unmatched_count += 1
                    continue

                # Definiere den vollständigen Zielpfad: BASIS / BUCHSTABE / PROMINENTENNAME
                # Beispiel: e:\Bilder\Celebrities\J\Jasmin Schwiers
                destination_folder = os.path.join(base_destination_folder, first_letter, celeb_name)

                # Zielordnerstruktur erstellen
                # os.makedirs erstellt auch alle übergeordneten Ordner (J)
                # exist_ok=True verhindert einen Fehler, wenn der Ordner (z.B. J und Jasmin Schwiers) bereits existiert
                try:
                    os.makedirs(destination_folder, exist_ok=True)
                except Exception as e:
                    print(f"  ⚠️ Fehler beim Erstellen des Zielordners '{destination_folder}': {e}")
                    unmatched_count += 1
                    continue

                # Endgültiger Zielpfad für die Datei
                final_destination = os.path.join(destination_folder, filename)

                # Datei verschieben
                try:
                    shutil.move(file_path, final_destination)
                    print(f"  🎉 VERSCHOBEN: '{filename}' -> '{os.path.join(first_letter, celeb_name)}'")
                    moved_count += 1
                except Exception as e:
                    print(f"  ⚠️ Fehler beim Verschieben von '{filename}': {e}")
                    unmatched_count += 1

            else:
                print(f"  ❌ Keine Übereinstimmung: Name in den Klammern ist leer. Datei: '{filename}'")
                unmatched_count += 1

        else:
            print(f"  ❌ Keine Übereinstimmung: Name in eckigen Klammern nicht gefunden. Datei: '{filename}'")
            unmatched_count += 1

print("\n------------------------------------------------\n")
print(f"Vorgang abgeschlossen.")
print(f"  {moved_count} Dateien wurden verschoben.")
print(f"  {unmatched_count} Dateien konnten nicht sortiert werden.")