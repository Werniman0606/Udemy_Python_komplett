import os
import filetype

# Konfigurieren des zu durchsuchenden Ordners
# Ändern Sie diesen Pfad, wenn Ihr Ordner woanders liegt
ROOT_FOLDER = r"/run/media/marco/Laufwerk D"


def get_real_extension(filepath):
    """
    Bestimmt die korrekte Dateierweiterung basierend auf dem Dateityp.
    """
    try:
        # Ermittelt den Dateityp der Datei
        kind = filetype.guess(filepath)
        if kind is not None:
            return kind.extension
        return None
    except Exception as e:
        print(f"Fehler beim Ermitteln des Dateityps für {filepath}: {e}")
        return None


def rename_file(filepath, new_extension):
    """
    Benennt die Datei um, falls die Endung nicht mit dem tatsächlichen
    Dateityp übereinstimmt.
    """
    current_name, current_extension = os.path.splitext(filepath)
    current_extension = current_extension.lstrip('.')

    if current_extension.lower() != new_extension.lower():
        # Konstruiert den neuen Dateipfad
        new_filepath = f"{current_name}.{new_extension}"

        # Benennt die Datei um
        try:
            os.rename(filepath, new_filepath)
            print(f"Umbenannt: '{os.path.basename(filepath)}' -> '{os.path.basename(new_filepath)}'")
            return True
        except FileExistsError:
            print(
                f"WARNUNG: Umbenennung von '{os.path.basename(filepath)}' fehlgeschlagen, da '{os.path.basename(new_filepath)}' bereits existiert.")
            return False
        except Exception as e:
            print(f"FEHLER beim Umbenennen von '{os.path.basename(filepath)}': {e}")
            return False
    return False


def main():
    """
    Hauptfunktion, die den Ordner durchläuft und Dateien verarbeitet.
    """
    # Überprüft, ob der Ordner existiert
    if not os.path.isdir(ROOT_FOLDER):
        print(f"Fehler: Der angegebene Ordner '{ROOT_FOLDER}' existiert nicht.")
        return

    print(f"Starte die Überprüfung und Umbenennung in '{ROOT_FOLDER}'...")
    renamed_count = 0

    # Durchläuft den Ordner und alle Unterordner
    for dirpath, dirnames, filenames in os.walk(ROOT_FOLDER):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            # Überprüft, ob die Datei eine bekannte Bild- oder Mediendatei ist
            if not any(filename.lower().endswith(ext) for ext in
                       ('.jpg', '.jpeg', '.gif', '.png', '.bmp', '.mp4', '.mov', '.mkv')):
                continue

            real_extension = get_real_extension(filepath)

            if real_extension:
                if rename_file(filepath, real_extension):
                    renamed_count += 1

    print("-" * 50)
    print(f"Überprüfung abgeschlossen.")
    print(f"Anzahl umbenannter Dateien: {renamed_count}")
    print("-" * 50)


if __name__ == "__main__":
    main()