# ==============================================================================
# Dateiname Vorschlag (Deutsch): tagging_fehler_in_datei_finden_verschieben.py
# Dateiname Vorschlag (Technisch): intra_file_tag_inconsistency_quarantine.py
#
# Beschreibung: Sucht nach Dateien, die in ihrem Präfix [TAG1, TAG2]_... zwei
#               sehr ähnliche Namen enthalten (Tippfehler). Die gefundenen Dateien
#               werden in einen Quarantäne-Ordner verschoben, wobei die
#               ursprüngliche Unterordnerstruktur beibehalten wird.
# ==============================================================================

import os
import re
import shutil
from fuzzywuzzy import fuzz  # Benötigt: pip install fuzzywuzzy python-Levenshtein
from collections import defaultdict

# --- Konfiguration ---
# Der Hauptordner, der rekursiv nach fehlerhaften Dateien durchsucht werden soll
ROOT_FOLDER = r"e:\Bilder\Celebrities"

# Der Zielordner, in den die fehlerhaften Dateien verschoben werden
DUPLICATE_QUARANTINE = r"e:\Personenduplikate"

# Ähnlichkeitsschwelle (Score von 0 bis 100).
# Ein Wert über 88 deutet stark auf einen Tippfehler hin.
SIMILARITY_THRESHOLD = 88


# ---------------------


def extract_persons_from_filename(filename):
    """
    Extrahiert die durch Komma getrennten Personennamen aus dem Präfix
    '[Person1, Person2]_...' und gibt sie als Liste zurück, falls es mehr als einen Namen gibt.
    """
    # Regex sucht nach: Start, [, beliebige Zeichen, bis zum ], gefolgt von _
    match = re.match(r'^\[(.+?)\]_', filename)
    if match:
        prefix_content = match.group(1)
        persons = [name.strip() for name in prefix_content.split(',')]

        # Nur verarbeiten, wenn mehr als ein Name getaggt wurde
        if len(persons) > 1:
            return persons
    return []


def move_to_quarantine(filepath, root_folder, quarantine_dir):
    """
    Verschiebt die Datei in den Quarantäne-Ordner und behält die Ordnerstruktur bei.

    Beispiel:
    filepath: e:\Bilder\Celebrities\A\Anna\file.jpg
    root_folder: e:\Bilder\Celebrities
    quarantine_dir: e:\Personenduplikate

    Zielpfad: e:\Personenduplikate\A\Anna\file.jpg
    """
    # Bestimme den relativen Pfad von der ROOT_FOLDER zum Ordner der Datei
    relative_dir = os.path.relpath(os.path.dirname(filepath), root_folder)

    # Konstruiere den vollständigen Zielordnerpfad im Quarantäne-Verzeichnis
    destination_dir = os.path.join(quarantine_dir, relative_dir)

    # Der vollständige Zielpfad für die Datei
    destination_path = os.path.join(destination_dir, os.path.basename(filepath))

    # 1. Zielordner erstellen (rekursiv)
    os.makedirs(destination_dir, exist_ok=True)

    # 2. Datei verschieben
    try:
        shutil.move(filepath, destination_path)
        return True, destination_path
    except Exception as e:
        print(f"  ❌ FEHLER beim Verschieben von '{os.path.basename(filepath)}': {e}")
        return False, None


def find_intra_file_inconsistencies(root_dir, quarantine_dir):
    """
    Durchsucht alle Dateien, extrahiert die Tags, vergleicht diese intern und verschiebt Fehler.
    """
    print(f"Starte Suche nach internen Tag-Inkonsistenzen in '{root_dir}'...")
    print(f"Gefundene Fehler werden verschoben nach: '{quarantine_dir}'")
    inconsistent_files = {}  # Speichert {Dateipfad: Liste von Fehlermeldungen}
    checked_count = 0
    moved_count = 0

    if not os.path.isdir(root_dir):
        print(f"Fehler: Der Hauptordner '{root_dir}' existiert nicht.")
        return inconsistent_files, 0, 0

    # Liste von Dateien, die verschoben werden sollen (muss nach os.walk passieren, da sich der Pfad ändert)
    files_to_move = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Nur relevante Bilddateien prüfen
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                continue

            persons = extract_persons_from_filename(filename)

            # Nur Dateien mit mindestens zwei Tags weiterverarbeiten
            if len(persons) < 2:
                continue

            filepath = os.path.join(dirpath, filename)
            checked_count += 1

            # --- Paarweiser Vergleich der Namen in der *selben* Datei ---

            n = len(persons)
            file_errors = []

            for i in range(n):
                for j in range(i + 1, n):
                    name1 = persons[i]
                    name2 = persons[j]

                    score = fuzz.ratio(name1.lower(), name2.lower())

                    if score >= SIMILARITY_THRESHOLD:
                        file_errors.append({
                            'name1': name1,
                            'name2': name2,
                            'score': score
                        })

            if file_errors:
                inconsistent_files[filepath] = file_errors
                # Füge den Pfad der fehlerhaften Datei zur Liste der zu verschiebenden Dateien hinzu
                files_to_move.append(filepath)

    # --- 2. Dateien verschieben ---
    if files_to_move:
        print("\n--- Verschiebe fehlerhafte Dateien in Quarantäne ---")
        for filepath in files_to_move:
            success, dest_path = move_to_quarantine(filepath, root_dir, quarantine_dir)
            if success:
                moved_count += 1
                print(f"  ✅ VERSCHOBEN: {os.path.basename(filepath)}")
            else:
                # Fehler beim Verschieben (wird in move_to_quarantine protokolliert)
                pass

    return inconsistent_files, checked_count, moved_count


def main():
    """
    Hauptfunktion zur Erkennung ähnlicher Namen innerhalb einer Datei und Verschiebung.
    """
    try:
        inconsistent_files, checked_count, moved_count = find_intra_file_inconsistencies(
            ROOT_FOLDER, DUPLICATE_QUARANTINE
        )

        print("\n" + "=" * 80)
        print("🚨 ZUSAMMENFASSUNG: Dateien mit internen Tag-Inkonsistenzen")
        print(f"Geprüfte Dateien mit 2+ Tags: {checked_count}")
        print(f"Gefundene Inkonsistenzen: {len(inconsistent_files)}")
        print(f"Dateien in Quarantäne verschoben: {moved_count}")
        print("=" * 80)

        if not inconsistent_files:
            print("Keine Dateien mit extrem ähnlichen, mehrfach getaggten Namen gefunden. 🎉")
            return

        # Ausgabe der Details (optional)
        print("\n--- Details der gefundenen Fehler ---")

        for original_filepath, errors in inconsistent_files.items():
            # Da die Datei verschoben wurde, zeigen wir den ursprünglichen Pfad und das Verschiebeziel an

            # Wir müssen den neuen Pfad rekonstruieren, da die Datei nicht mehr am Originalort ist
            relative_dir = os.path.relpath(os.path.dirname(original_filepath), ROOT_FOLDER)
            quarantine_path = os.path.join(DUPLICATE_QUARANTINE, relative_dir, os.path.basename(original_filepath))

            print(f"\n📁 Ursprünglicher Pfad: {os.path.dirname(original_filepath)}")
            print(f"   Verschoben nach: {os.path.dirname(quarantine_path)}")

            for error in errors:
                print(
                    f"  ❌ FEHLER im Dateinamen **{os.path.basename(original_filepath)}**: '{error['name1']}' vs. '{error['name2']}'")
                print(f"     Ähnlichkeit (Fuzz Ratio): {error['score']}/100")

        print("\n" + "=" * 80)
        print("Aktion: Bitte überprüfen Sie die Dateien im Quarantäne-Ordner.")

    except ImportError:
        print("\n--- FEHLER: Bibliothek 'fuzzywuzzy' fehlt ---")
        print("Bitte installieren Sie die benötigte Bibliothek mit: **pip install fuzzywuzzy python-Levenshtein**")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    main()