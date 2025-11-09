# ==============================================================================
# Dateiname Vorschlag (Deutsch): dateien_nach_muster_in_chaosordner_verschieben.py
# Dateiname Vorschlag (Technisch): file_pattern_chaos_mover.py
#
# Beschreibung: Dieses Skript dient der Bereinigung eines Quellordners, indem
#               es Dateien, die zwei spezifischen "Chaos-Mustern" folgen, in einen
#               neu erstellten Unterordner namens 'Chaos' verschiebt.
#
#               Chaos-Muster:
#               1. Muster A: Dateiname enthält die Sequenz '-ZahlZahl-' (z.B. '-01-').
#               2. Muster B: Dateiname enthält nur EINEN Bindestrich und endet
#                  auf '1.Dateiendung' (z.B. 'Name-Suffix1.jpg').
#
#               Alle anderen Dateien, die vermutlich einem korrekten Namensstandard
#               entsprechen (z.B. Name/Jahr), bleiben im Quellordner.
# ==============================================================================

import os
import shutil
import re

# --- Konfiguration ---
# Der Ordner, der die zu sortierenden Dateien enthält (z.B. 'Vintage')
source_directory = r'e:\Bilder\Celebrities\V\Vintage'
# Der Name des Unterordners, in den die "Chaos"-Dateien verschoben werden
chaos_directory_name = 'Chaos'
# Der vollständige Zielpfad (wird automatisch erstellt: source_directory/Chaos)
destination_directory = os.path.join(source_directory, chaos_directory_name)
# ---------------------

# Muster zur Identifizierung von Chaos-Dateien (die verschoben werden sollen):

# Muster A (Zahl-Muster, z.B. -02-):
# Sucht nach einem Bindestrich, gefolgt von zwei Ziffern, gefolgt von einem Bindestrich.
pattern_a = re.compile(r'-\d{2}-')

# Muster B (Endet auf 1, nur ein Bindestrich vor dem Ende):
# ^[^-]+-        : Start der Datei, gefolgt von beliebigen Zeichen OHNE Bindestrich, dann einem Bindestrich.
# [^-]+1\.\w+$   : Gefolgt von beliebigen Zeichen OHNE Bindestrich, endend auf '1.Dateiendung'.
# Stellt sicher, dass die Datei exakt einen Bindestrich enthält und auf '1' endet.
pattern_b = re.compile(r'^[^-]+-[^-]+1\.\w+$', re.IGNORECASE)

# Erstelle den Chaos-Unterordner, falls er nicht existiert
os.makedirs(destination_directory, exist_ok=True)
print(f"Zielordner für 'Chaos' erstellt: {destination_directory}\n")

moved_count = 0
skipped_count = 0

for filename in os.listdir(source_directory):
    source_path = os.path.join(source_directory, filename)

    # Stelle sicher, dass wir nur reguläre Dateien bearbeiten und nicht den 'Chaos'-Ordner selbst
    if os.path.isfile(source_path):

        should_be_moved = False

        # Prüfe Muster A: Datei enthält '-ZahlZahl-'
        if pattern_a.search(filename):
            should_be_moved = True

        # Prüfe Muster B: Datei hat exakt einen Bindestrich und endet auf '1.Endung'
        if pattern_b.search(filename):
            should_be_moved = True

        if should_be_moved:
            # Wenn eines der Chaos-Muster zutrifft, wird die Datei verschoben
            destination_path = os.path.join(destination_directory, filename)

            try:
                # Prüfen, ob die Zieldatei bereits existiert (wichtig bei mehreren Durchläufen)
                if os.path.exists(destination_path):
                    print(f"SKIPPED (Ziel existiert): {filename}")
                    skipped_count += 1
                    continue

                # Verschieben der Datei
                shutil.move(source_path, destination_path)
                print(f"✅ MOVED (Chaos): {filename}")
                moved_count += 1
            except Exception as e:
                print(f"❌ Error moving {filename}: {e}")
        else:
            # Wenn keines der Chaos-Muster zutrifft, ist es eine 'gute' Datei
            print(f"➡️ SKIPPED (Behalten): {filename}")
            skipped_count += 1

print(f"\n--- Prozess abgeschlossen! ---")
print(f"Dateien verschoben (Chaos-Muster): {moved_count}")
print(f"Dateien übersprungen (Behalten): {skipped_count}")

Would you like to try running this process on a different directory or define a new set of 'Chaos' patterns?