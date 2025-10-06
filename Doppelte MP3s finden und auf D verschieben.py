import os
import shutil
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError

# --- KONFIGURATION ---
# 1. Quelle: Hier liegen die NEUEN Songs (Referenz für die Duplikat-Suche)
SOURCE_DIR = r"d:\extracted\Duets"

# 2. Archive: Die Liste der Basisordner der Musiksammlung (werden durchsucht)
ARCHIVE_DIRS = [
    r"z:\MP3s\A-D",
    r"z:\MP3s\E-L",
    r"z:\MP3s\M-R",
    r"z:\MP3s\S-Z",
    r"z:\MP3s\Country",
]

# 3. Ziel: Hierhin werden die Duplikate aus den Archiven VERSCHOBEN
DUPLICATE_TARGET_DIR = r"d:\extracted\Dubletten"


# ---------------------

def normalize_tag(tag_value):
    """
    Normalisiert einen ID3-Tag-Wert zur besseren Vergleichbarkeit.
    Wandelt in Kleinbuchstaben um und entfernt gängige Satzzeichen,
    die in Tags variieren können (z.B. ' vs. ´).
    """
    if not tag_value:
        return ""

    value = str(tag_value[0]).strip().lower()

    # Entfernt gängige Satzzeichen für einen robusten Vergleich
    for char in ["'", "`", "’", "´", ".", ","]:
        value = value.replace(char, "")

    return value.replace(" ", "")  # Entfernt auch Leerzeichen für höchste Toleranz


def get_mp3_tags(file_path):
    """
    Liest Interpret (TPE1) und Titel (TIT2) aus MP3-Datei aus und normalisiert sie.
    """
    try:
        audio = MP3(file_path)
        # Verwenden Sie die Mutagen-Schlüssel
        artist = audio.get('TPE1', [''])[0]
        title = audio.get('TIT2', [''])[0]

        # Erstellt den Schlüssel (Artist, Title)
        key = (normalize_tag([artist]), normalize_tag([title]))

        if all(key):  # Nur wenn Artist UND Title erfolgreich ausgelesen wurden
            return key

    except ID3NoHeaderError:
        # Datei hat keine ID3-Tags (wird ignoriert)
        pass
    except Exception as e:
        print(f"Fehler beim Lesen der Tags von {os.path.basename(file_path)}: {e}")

    return None


def find_and_move_duplicates(source_dir, archive_dirs, target_dir):
    """
    Hauptfunktion: Erstellt Referenz-DB, sucht Duplikate im Archiv und verschiebt sie.
    """

    # 1. Datenbank der Referenzsongs (Quellordner) erstellen
    reference_keys = set()
    print("=" * 70)
    print(f"Phase 1: Erstelle Referenz-Datenbank aus {source_dir}...")

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.mp3'):
                key = get_mp3_tags(os.path.join(root, file))
                if key:
                    reference_keys.add(key)

    if not reference_keys:
        print("Keine gültigen Interpret-Titel-Kombinationen in der Quelle gefunden. Vorgang abgebrochen.")
        return

    print(f"-> Referenz-Datenbank erstellt. {len(reference_keys)} eindeutige Songs gefunden.")

    # Zielordner erstellen
    os.makedirs(target_dir, exist_ok=True)
    moved_count = 0

    # 2. Archive rekursiv durchsuchen und Duplikate verschieben
    print("\nPhase 2: Durchsuche Archive nach Duplikaten und verschiebe sie...")

    for base_archive in archive_dirs:
        archive_name = os.path.basename(base_archive)
        print(f"  > Prüfe Archiv-Basisordner: {base_archive}")

        for root, _, files in os.walk(base_archive):
            for file in files:
                if file.lower().endswith('.mp3'):
                    archive_path = os.path.join(root, file)
                    archive_key = get_mp3_tags(archive_path)

                    # 3. Vergleichen und Verschieben
                    if archive_key and archive_key in reference_keys:

                        # Die Unterordner-Struktur relativ zum Basisarchiv ermitteln
                        # Bsp: 'z:\MP3s\M-R' ist Basis; 'Michael Jackson' ist relativ
                        relative_path = os.path.relpath(root, base_archive)

                        # Zielpfad erstellen: d:\extracted\Dubletten\M-R\Michael Jackson\...
                        target_sub_dir = os.path.join(target_dir, archive_name, relative_path)
                        os.makedirs(target_sub_dir, exist_ok=True)

                        target_full_path = os.path.join(target_sub_dir, file)

                        try:
                            # !!! WICHTIG: Die Datei wird VERSCHOBEN (shutil.move) !!!
                            shutil.move(archive_path, target_full_path)

                            print(f"  [VERSCHOBEN] '{file}' von '{root}'")
                            moved_count += 1
                        except Exception as e:
                            print(f"  [FEHLER] Konnte {archive_path} nicht verschieben: {e}")

    print("\n" + "=" * 70)
    print("--- Duplikat-Vorgang abgeschlossen ---")
    print(f"Gesamt: {moved_count} Duplikate im Archiv gefunden und verschoben.")
    print("Bitte überprüfen Sie den Ordner '{DUPLICATE_TARGET_DIR}'.")
    print("=" * 70)


# Skript ausführen
find_and_move_duplicates(SOURCE_DIR, ARCHIVE_DIRS, DUPLICATE_TARGET_DIR)