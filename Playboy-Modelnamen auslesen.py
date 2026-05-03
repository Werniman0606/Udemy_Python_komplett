import os
import shutil


def rename_images_with_model_name():
    # Dein festgelegter Zielpfad
    directory = r'd:\extracted\rips'

    # Prüfen, ob das Verzeichnis existiert
    if not os.path.exists(directory):
        print(f"Fehler: Das Verzeichnis {directory} wurde nicht gefunden.")
        return

    count = 0

    # Alle Dateien im Ordner durchlaufen
    for filename in os.listdir(directory):
        # Nur Bilddateien verarbeiten (optional, filtert nach Endungen)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            try:
                # Trennung am Bindestrich
                # Format: "ID-Name-ID.ext"
                parts = filename.split('-')

                # Sicherstellen, dass mindestens zwei Bindestriche vorhanden sind
                if len(parts) >= 3:
                    model_name = parts[1].strip()
                    new_filename = f"[{model_name}]_{filename}"

                    old_file = os.path.join(directory, filename)
                    new_file = os.path.join(directory, new_filename)

                    # Umbenennung durchführen
                    os.rename(old_file, new_file)
                    count += 1
                    print(f"Umbenannt: {filename} -> {new_filename}")
                else:
                    print(f"Übersprungen (falsches Format): {filename}")

            except Exception as e:
                print(f"Fehler bei Datei {filename}: {e}")

    print(f"\nFertig! Es wurden {count} Dateien erfolgreich umbenannt.")


if __name__ == "__main__":
    rename_images_with_model_name()