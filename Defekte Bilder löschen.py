import os
import subprocess
import time

# --- KONFIGURATION START ---
# Pfad zu exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Basisverzeichnis, in dem nach Bildern gesucht werden soll
SOURCE_DIR = r'd:\extracted\rips'

# Erlaubte Bildformate
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg')

# Minimale Dateigröße in Bytes. Dateien, die kleiner sind, werden als potenziell defekt markiert.
# Sie können diesen Wert anpassen, je nach Ihren Bildern.
MINIMUM_FILE_SIZE = 1024  # 1 KB


# --- KONFIGURATION ENDE ---

def check_for_critical_errors(file_path):
    """
    Prüft eine Bilddatei mit Exiftool auf kritische Fehler.
    Analysiert die gesamte Ausgabe, um visuelle Defekte zu erkennen.
    """
    command = [EXIFTOOL_PATH, '-validate', file_path]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            encoding='utf-8',
            errors='ignore'
        )

        output = (result.stdout + result.stderr).lower()

        critical_keywords = [
            "bad end of image",
            "truncated file",
            "corrupted file",
            "damaged file",
            "missing jpeg sos marker",
            "error",
        ]

        if any(keyword in output for keyword in critical_keywords):
            print(f"⚠️ KRITISCHER FEHLER (Exiftool) gefunden in: {file_path}")
            print(f"   Exiftool-Ausgabe: {output.strip()}")
            return True

        if result.returncode != 0 and "warning" not in output:
            print(f"⚠️ Exiftool gab einen Fehlercode ({result.returncode}) zurück für: {file_path}")
            print(f"   Exiftool-Ausgabe: {output.strip()}")
            return True

        return False

    except FileNotFoundError:
        print(f"❌ Fehler: Exiftool-Pfad '{EXIFTOOL_PATH}' ist ungültig. Skript wird beendet.")
        return False
    except Exception as e:
        print(f"❌ Unerwarteter Fehler bei der Prüfung von '{file_path}': {e}")
        return False


def check_file_size(file_path):
    """
    Prüft, ob die Dateigröße über einem bestimmten Minimum liegt.
    """
    if os.path.getsize(file_path) < MINIMUM_FILE_SIZE:
        print(f"⚠️ Datei ist zu klein ({os.path.getsize(file_path)} Bytes). Potenziell defekt: {file_path}")
        return True
    return False


def main():
    print("Starte die Suche nach defekten Bildern...")
    print(f"Durchsuche Ordner: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Fehler: Quellverzeichnis '{SOURCE_DIR}' nicht gefunden.")
        return

    if not os.path.isfile(EXIFTOOL_PATH):
        print(f"❌ Fehler: Exiftool-Pfad '{EXIFTOOL_PATH}' ist ungültig. Skript wird beendet.")
        return

    files_to_delete = []
    checked_count = 0
    start_time = time.time()

    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)

            if file.lower().endswith(ALLOWED_EXTENSIONS):
                checked_count += 1

                # Führt beide Prüfungen durch
                if check_for_critical_errors(file_path) or check_file_size(file_path):
                    print(f"❗ Defektes Bild gefunden: {file_path}")
                    files_to_delete.append(file_path)
                else:
                    print(f"✅ {file_path} scheint in Ordnung zu sein.")

    print("\n---")
    print(f"Prüfung abgeschlossen. {len(files_to_delete)} Dateien werden gelöscht.")
    print("Starte den Löschvorgang...")

    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"✅ Gelöscht: {file_path}")
        except Exception as e:
            print(f"❌ Fehler beim Löschen von '{file_path}': {e}")

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Vorgang abgeschlossen.")
    print(f"Insgesamt {checked_count} Dateien überprüft.")
    print(f"Insgesamt {len(files_to_delete)} defekte Dateien gelöscht.")
    print(f"Dauer: {duration:.2f} Sekunden")


if __name__ == '__main__':
    main()