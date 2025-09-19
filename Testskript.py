import os
import time

# Dein Quellverzeichnis
SOURCE_DIR = r'e:\Bilder\Celebrities\C\Chloe Morgane'


def main():
    print(f"Starte die Dateisuche in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Fehler: Quellverzeichnis '{SOURCE_DIR}' nicht gefunden.")
        return

    found_files = []
    start_time = time.time()

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
        print(f"✅ Das Skript hat Dateien gefunden. Hier sind die ersten 20:")
        for file_path in found_files:
            print(f"- {file_path}")

    print(f"\n---")
    print(f"Dauer der Suche: {duration:.2f} Sekunden")
    print("Vorgang abgeschlossen.")


if __name__ == '__main__':
    main()