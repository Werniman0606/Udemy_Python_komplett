# ==============================================================================
# Dateiname Vorschlag (Deutsch): dateiname_prefix_aus_name_setzen.py
# Dateiname Vorschlag (Technisch): rename_prefix_from_content.py
#
# Beschreibung: Dieses Skript durchsucht ein Verzeichnis und benennt Dateien um,
#               die einem spezifischen Muster entsprechen: '[XXXX]-Vorname Nachname...'.
#               Es extrahiert den 'Vorname Nachname'-Teil nach dem ersten Bindestrich
#               und fügt diesen in eckigen Klammern als Präfix vor den
#               ursprünglichen Dateinamen ein.
#               (Beispiel: XXX-Max Mustermann-Y.jpg wird zu [Max Mustermann]_XXX-Max Mustermann-Y.jpg).
#               Dateien, bei denen das Namensmuster nicht gefunden wird, werden übersprungen.
# ==============================================================================

import os
import re

# --- Konfiguration ---
source_directory = r'd:\Bilder'  # Das Verzeichnis, in dem die umzubenennenden Dateien liegen
# ---------------------

# Alternativ (einfacher und robuster): Wir extrahieren einfach die ersten beiden Wörter
# nach dem ersten Bindestrich und ignorieren den Rest bis zur Endung.
# Hier gehen wir von einem Format wie: XXXX-Vorname NachnameRest-YYYY.ext aus.
# ^[^-]+- : Sucht vom Anfang bis zum ersten Bindestrich
# ([a-zA-Z]+) : Gruppe 1 (Vorname)
# \s+ : Ein oder mehr Leerzeichen
# ([a-zA-Z]+) : Gruppe 2 (Nachname)
# .* : Der Rest der Zeichenkette
flexible_name_pattern = re.compile(r'^[^-]+-([a-zA-Z]+)\s+([a-zA-Z]+).*', re.IGNORECASE)

print(f"Starte Umbenennung im Verzeichnis: {source_directory}\n")

renamed_count = 0
skipped_count = 0

for filename in os.listdir(source_directory):
    source_path = os.path.join(source_directory, filename)

    # Stelle sicher, dass wir nur reguläre Dateien bearbeiten
    if os.path.isfile(source_path):

        match = flexible_name_pattern.search(filename)

        if match:
            # Gruppe 1 ist der Vorname, Gruppe 2 ist der Nachname
            first_name = match.group(1)
            last_name = match.group(2)
            extracted_name = f"{first_name} {last_name}"

            # 1. Der neue Dateiname: [Vorname Nachname]_Originaldateiname
            new_filename = f"[{extracted_name}]_" + filename

            # 2. Pfade für die Umbenennung
            old_path = source_path
            new_path = os.path.join(source_directory, new_filename)

            # --- Prüfen auf bereits existierenden, korrekten Präfix ---
            # Prüfen, ob die Datei bereits den neu generierten Präfix trägt
            if filename.startswith(f"[{extracted_name}]_"):
                print(f"SKIPPED (Bereits getaggt mit korrektem Präfix): {filename}")
                skipped_count += 1
                continue

            try:
                # Prüfen, ob die Zieldatei bereits existiert (wichtig bei mehreren Durchläufen)
                if os.path.exists(new_path):
                    print(f"SKIPPED (Ziel existiert bereits): {filename}")
                    skipped_count += 1
                    continue

                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
                renamed_count += 1

            except Exception as e:
                print(f"Error renaming {filename}: {e}")
                skipped_count += 1

        else:
            print(f"SKIPPED (Namensmuster nicht gefunden): {filename}")
            skipped_count += 1

print(f"\n--- Prozess abgeschlossen! ---")
print(f"Dateien umbenannt: {renamed_count}")
print(f"Dateien übersprungen: {skipped_count}")