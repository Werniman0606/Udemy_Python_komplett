import os
import shutil
import re

# --- Konfiguration ---
source_directory = r'e:\Bilder\Celebrities\V\Vintage'
celebrities_root = r'e:\Bilder\Celebrities'
destination_directory = r'd:\Bilder'


# ---------------------

def get_comparison_names(root_dir):
    """
    Durchsucht alle Unterordner unter root_dir und extrahiert das erste Wort des Ordnernamens.
    Gibt ein Set von eindeutigen, in Kleinbuchstaben konvertierten Wörtern zurück.
    """
    comparison_names = set()
    print(f"Scanne die Ordnerstruktur unter: {root_dir}...")

    # os.walk durchläuft das gesamte Verzeichnis und alle Unterverzeichnisse
    for root, dirs, files in os.walk(root_dir):
        for dir_name in dirs:
            # Das erste Wort des Ordnernamens extrahieren und in Kleinbuchstaben umwandeln
            # Z.B. 'Laura Misch' -> 'Laura'
            first_word = dir_name.split(' ')[0]
            if first_word:
                comparison_names.add(first_word.lower())

    print(f"Insgesamt {len(comparison_names)} eindeutige Namen zur Validierung gefunden.")
    return comparison_names


def extract_first_name_from_filename(filename):
    """
    Extrahiert den potenziellen Vornamen aus dem Dateinamen.
    Basierend auf dem Format: Praefix-Vorname Nachname...-Suffix.
    """
    try:
        # Teile den Dateinamen am ersten Bindestrich
        parts = filename.split('-', 1)
        if len(parts) < 2:
            return None

        # Der Rest des Namens (z.B. 'Laura Misch-18ax73gbk2zf1.jpg')
        name_part_full = parts[1]

        # Finde das Ende des Namens vor dem nächsten Bindestrich oder dem Punkt der Endung
        match = re.match(r'(.+?)(-\w+)?\.\w+$', name_part_full)
        if not match:
            # Wenn das Muster nicht greift (unerwartetes Format), den gesamten Rest nehmen
            name_and_suffix = name_part_full
        else:
            # Die Gruppe 1 ist der Namensteil vor der Endung (z.B. 'Laura Misch')
            name_and_suffix = match.group(1).strip()

        # Das erste Wort des Namens ist der Vorname
        first_word = name_and_suffix.split(' ')[0]

        return first_word.lower()
    except Exception:
        return None


# --- Hauptprogramm ---

# 1. Vorbereitung des Zielordners
os.makedirs(destination_directory, exist_ok=True)

# 2. Sammeln der Validierungsnamen
valid_first_names = get_comparison_names(celebrities_root)

# 3. Dateien durchgehen und verschieben
moved_count = 0
skipped_count = 0
error_count = 0

print(f"\nStarte den Abgleich in: {source_directory}\n")

for filename in os.listdir(source_directory):
    source_path = os.path.join(source_directory, filename)

    if os.path.isfile(source_path):

        # Name aus der Datei extrahieren (in Kleinbuchstaben)
        file_first_name = extract_first_name_from_filename(filename)

        if file_first_name and file_first_name in valid_first_names:
            # Übereinstimmung gefunden! Verschieben.
            destination_path = os.path.join(destination_directory, filename)

            try:
                # Sicherstellen, dass die Datei im Ziel nicht bereits existiert
                if os.path.exists(destination_path):
                    print(f"SKIPPED (Ziel existiert): {filename}")
                    skipped_count += 1
                    continue

                shutil.move(source_path, destination_path)
                print(f"MOVED (Match: {file_first_name}): {filename}")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {filename}: {e}")
                error_count += 1
        else:
            # Keine Übereinstimmung gefunden oder Name konnte nicht extrahiert werden
            print(f"SKIPPED (Kein Match): {filename}")
            skipped_count += 1

print("\n--- Prozess abgeschlossen! ---")
print(f"Dateien verschoben (Namens-Match): {moved_count}")
print(f"Dateien übersprungen (Kein Match oder bereits vorhanden): {skipped_count}")
print(f"Fehler beim Verschieben: {error_count}")