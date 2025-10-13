import os
import time
from collections import defaultdict

# --- Konfiguration ---
# Der HAUPT-Archivordner, der REKURSIV (inkl. Unterordner) geprüft wird
BASE_ARCHIVE_DIR = r"z:\Gepackte Programme\bereit installiert"
# ---------------------

# Blacklist von Dateien, die ignoriert werden sollen (nicht als Installer gelten)
FILENAME_BLACKLIST = [
    'patchmypc.log',
    'pmp-helper.exe',
    'temp',
    'desktop.ini',
    'thumbs.db'
]


def get_program_id(filename):
    """
    Erstellt eine präzisere ID aus den ersten Teilen des Dateinamens.
    """
    base_name = os.path.splitext(filename)[0].lower()
    name_parts = [part.strip() for part in base_name.split('_') if part.strip()]

    if not name_parts:
        return ""

    # Wir verwenden die ersten beiden Teile der Datei als ID
    id_parts = name_parts[:2]

    return "_".join(id_parts)


def clean_duplicate_versions_manual(base_dir):
    """
    Durchsucht den Basisordner REKURSIV und bietet eine manuelle Auswahl der zu behaltenden Datei.
    """
    print("=" * 80)
    print(f"Starte MANUELLE Duplikatbereinigung in: {base_dir}")
    print("WARNUNG: Alle Entscheidungen über die zu behaltende Datei werden JETZT von Ihnen getroffen.")
    print("=" * 80)

    # Mapping: Programm-ID -> Liste von Pfaden der Dateien
    files_by_id = defaultdict(list)
    deleted_count = 0

    # 1. Dateien REKURSIV sammeln und nach Programm-ID gruppieren
    for root, _, files in os.walk(base_dir):
        for filename in files:
            full_path = os.path.join(root, filename)

            # Blacklist-Prüfung
            if any(bl_item.lower() in filename.lower() for bl_item in FILENAME_BLACKLIST):
                continue

            program_id = get_program_id(filename)
            files_by_id[program_id].append(full_path)

    # 2. Interaktives Löschen der alten Dateien
    for program_id, file_list in files_by_id.items():
        if len(file_list) <= 1:
            continue

        print("\n" + "#" * 80)
        print(f"Duplikat-Gruppe gefunden (ID: '{program_id}'):")
        print(f"Es wurden {len(file_list)} Dateien in verschiedenen Ordnern gefunden, die zu dieser ID passen.")
        print("-" * 80)

        # Dateien anzeigen und zur Auswahl nummerieren
        for i, path in enumerate(file_list):
            filename = os.path.basename(path)
            mtime = os.path.getmtime(path)

            print(f"  [{i + 1}] {filename}")
            print(f"      Ordner: {os.path.dirname(path)}")
            print(f"      Datum: {time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))}")

        # Manuelle Auswahl abfragen
        while True:
            prompt = f"\nWelche Datei soll BEHALTEN werden (Nummer 1 bis {len(file_list)}) oder 'N' für KEINE? "
            user_input = input(prompt).strip().upper()

            if user_input == 'N':
                print("  [ÜBERSPRUNGEN] Keine Datei aus dieser Gruppe wird gelöscht.")
                files_to_delete = []
                break

            try:
                # Konvertiere die Eingabe in einen Index (1 -> 0, 2 -> 1, etc.)
                selection_index = int(user_input) - 1
                if 0 <= selection_index < len(file_list):
                    # Die ausgewählte Datei ist die zu behaltende
                    file_to_keep = file_list[selection_index]

                    # Alle anderen Dateien sind die zu löschenden
                    files_to_delete = [p for i, p in enumerate(file_list) if i != selection_index]

                    print(f"\n-> Sie haben '{os.path.basename(file_to_keep)}' als zu behaltende Datei ausgewählt.")
                    break
                else:
                    print(
                        f"Ungültige Eingabe. Bitte geben Sie eine Nummer zwischen 1 und {len(file_list)} ein oder 'N'.")
            except ValueError:
                print(f"Ungültige Eingabe. Bitte geben Sie eine Nummer (1, 2, ...) oder 'N' ein.")

        # 3. Löschbestätigung und Ausführung
        if files_to_delete:
            print("\n" + "=" * 80)
            print(f"BESTÄTIGUNG: Sollen die folgenden {len(files_to_delete)} älteren/anderen Dateien GELÖSCHT werden?")
            for p in files_to_delete:
                print(f"  - {os.path.basename(p)} (im Ordner: {os.path.dirname(p)})")
            print("=" * 80)

            final_prompt = "  -> Endgültige Bestätigung zum Löschen aller aufgelisteten Dateien (J/N): "
            final_confirmation = input(final_prompt).strip().lower()

            if final_confirmation == 'j':
                for old_path in files_to_delete:
                    try:
                        os.remove(old_path)
                        print(f"  [LÖSCHEN ERFOLGREICH] {os.path.basename(old_path)} wurde entfernt.")
                        deleted_count += 1
                    except Exception as e:
                        print(f"  [FEHLER] Konnte {os.path.basename(old_path)} nicht löschen: {e}")
            else:
                print("  [AKTION ABGEBROCHEN] Keine Dateien gelöscht.")

    print("\n" + "=" * 80)
    print("--- Interaktive, manuelle Bereinigung abgeschlossen ---")
    print(f"Gesamt: {deleted_count} Installationsdateien wurden gelöscht.")
    print("=" * 80)


# Skript ausführen
clean_duplicate_versions_manual(BASE_ARCHIVE_DIR)