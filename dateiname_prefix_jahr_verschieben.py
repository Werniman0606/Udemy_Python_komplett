# ==============================================================================
# Dateiname Vorschlag (Deutsch): dateiname_prefix_jahr_verschieben.py
# Dateiname Vorschlag (Technisch): rename_prefix_by_year_move.py
#
# Beschreibung: Dieses Skript durchsucht ein Quellverzeichnis (SOURCE_DIRECTORY)
#               nach Dateien, die einem spezifischen Namensmuster folgen, das
#               eine Jahreszahl zwischen 1920 und 2000 (optional gefolgt von 's')
#               enthält (z.B. 'XXX-Max Mustermann 1980s-YYY.jpg').
#               1. Es extrahiert den Vor- und Nachnamen.
#               2. Es benennt die Datei um, indem es diesen Namen als Präfix
#                  in eckigen Klammern voranstellt (z.B. '[Max Mustermann]_XXX...').
#               3. Es verschiebt die umbenannte Datei in den Zielordner
#                  (DESTINATION_DIRECTORY).
# ==============================================================================

import os
import shutil
import re

# --- Konfiguration ---
source_directory = r'e:\Bilder\Celebrities\V\Vintage'
destination_directory = r'd:\Bilder'
# ---------------------

# Die Jahreszahl-Muster wurden aktualisiert, um ein optionales 's' (s?) zu berücksichtigen.

# 1. Regex zur Extraktion des Namen-Jahr-Teils:
# ^[a-zA-Z0-9]+-   : Start der Datei bis zum ersten Bindestrich.
# (.+?)             : Gruppe 1: Der Name (nicht-gierig)
# (19[2-9]\d|2000)s?: Gruppe 2: Das Jahr (1920-1999 oder 2000) mit optionalem 's'
# -                 : Das abschließende Trennzeichen.
name_year_pattern = re.compile(r'^[a-zA-Z0-9]+-(.+?) (19[2-9]\d|2000)s?-')

# Der Regex zur einfachen Verifizierung, dass das Jahr (mit oder ohne 's') enthalten ist.
# Dies stellt sicher, dass nur relevante Dateien bearbeitet werden.
year_check_pattern = re.compile(r'(19[2-9]\d|2000)s?-')

# Erstelle den Zielordner, falls er nicht existiert (für den Move-Vorgang)
os.makedirs(destination_directory, exist_ok=True)

print(f"Starte Umbenennung und Verschiebung in: {source_directory}")
print(f"Zielverzeichnis: {destination_directory}\n")

for filename in os.listdir(source_directory):
    source_path = os.path.join(source_directory, filename)

    # Stelle sicher, dass wir nur Dateien bearbeiten, die das Jahr (mit/ohne 's') enthalten
    if os.path.isfile(source_path) and year_check_pattern.search(filename):
        # Das Suchmuster wird nur angewendet, wenn die Jahresprüfung erfolgreich ist
        match = name_year_pattern.search(filename)

        if match:
            # Gruppe 1: Der gesamte Teil zwischen dem ersten Bindestrich und dem Jahr
            # (z.B. "Pamela Anderson " oder "Carol Nash - Private Love Affair ")
            name_part_full = match.group(1).strip()

            # Teile den extrahierten String in Wörter
            words = name_part_full.split()

            # Extrahiere nur die ersten beiden Wörter (Vorname Nachname)
            if len(words) >= 2:
                first_name = words[0]
                last_name = words[1]
                extracted_name = f"{first_name} {last_name}"
            else:
                # Fallback, wenn der Namensteil nur aus einem Wort besteht
                extracted_name = words[0] if words else "Unknown"

            # 1. Der neue Dateiname: [Vorname Nachname]_Originaldateiname
            new_filename = f"[{extracted_name}]_" + filename

            # Pfade für die Umbenennung und das Verschieben
            old_path_for_rename = source_path
            new_path_after_rename = os.path.join(source_directory, new_filename)
            destination_path = os.path.join(destination_directory, new_filename)

            try:
                # --- Schritt 1: Umbenennen im Quellverzeichnis ---
                # Dies ist notwendig, damit die Datei unter dem neuen Namen verschoben werden kann
                os.rename(old_path_for_rename, new_path_after_rename)
                print(f"✅ Renamed: {filename} -> {new_filename}")

                # --- Schritt 2: Verschieben in das Zielverzeichnis ---
                shutil.move(new_path_after_rename, destination_path)
                print(f"✅ Moved: {new_filename}")

            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

        else:
            print(f"➡️ Skip: Name/Jahr-Muster nicht gefunden (RegEx-Mismatch) in {filename}")

    # Dateien werden übersprungen, wenn sie das definierte Jahr nicht enthalten
    elif os.path.isfile(source_path):
        print(f"➡️ Skip: Jahr (1920-2000, mit oder ohne 's') nicht gefunden in {filename}")

print("\n--- Prozess abgeschlossen! ---")

Would you like me to help you draft another script, or perhaps refine the Regex used in this one?