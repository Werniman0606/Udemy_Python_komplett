# ==============================================================================
# Dateiname Vorschlag (Deutsch): dateisuche_pfad_ueberpruefung.py
# Dateiname Vorschlag (Technisch): recursive_file_path_checker.py
#
# Beschreibung: Dieses Diagnoseskript dient zur schnellen Überprüfung, ob ein
#               angegebener Quellpfad (SOURCE_DIR) existiert und ob darin Dateien
#               gefunden werden. Es durchsucht den Ordner rekursiv, misst die
#               benötigte Zeit und gibt zur Validierung die ersten 20 gefundenen
#               Dateipfade aus. Es führt keine Operationen wie Verschieben oder
#               Umbenennen durch.
# ==============================================================================

import os
import time

# --- Konfiguration ---
# Dein Quellverzeichnis, das rekursiv durchsucht werden soll
SOURCE_DIR = r'e:\Bilder\Celebrities\C\Chloe Morgane'
# ---------------------


def main():
    """
    Hauptfunktion: Durchsucht den SOURCE_DIR rekursiv und protokolliert die ersten Treffer.
    """
    print(f"Starte die rekursive Dateisuche in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Fehler: Quellverzeichnis '{SOURCE_DIR}' nicht gefunden.")
        return

    found_files = []
    start_time = time.time()

    # Durchläuft den Quellordner und alle Unterordner
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            # Speichere nur die ersten 20 gefundenen Dateien zur Übersicht
            if len(found_files) < 20:
                found_files.append(file_path)

    end_time = time.time()
    duration = end_time - start_time

    if not found_files:
        print("❌ Das Skript hat keine Dateien im angegebenen Pfad gefunden.")
    else:
        print(f"\n✅ Das Skript hat Dateien gefunden. Hier sind die ersten {len(found_files)}:")
        for file_path in found_files:
            print(f"- {file_path}")

    print(f"\n---")
    print(f"Dauer der Suche: {duration:.2f} Sekunden")
    print("Vorgang abgeschlossen.")


if __name__ == '__main__':
    main()