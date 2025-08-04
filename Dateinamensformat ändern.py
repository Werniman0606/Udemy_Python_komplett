import os

# --- KONFIGURATION START ---
# Der Ordner, in dem die Bilder liegen.
# HINWEIS: Setzen Sie hier den korrekten Pfad zu Ihrem Ordner ein.
FOLDER_PATH = r'e:\Bilder2\Girls'


# --- KONFIGURATION ENDE ---

def rename_files(folder):
    """
    Durchsucht einen Ordner nach Bilddateien und benennt sie um,
    indem die Anfangsbuchstaben von Vor- und Nachnamen in Großbuchstaben umgewandelt werden.
    """
    if not os.path.isdir(folder):
        print(f"Fehler: Der angegebene Ordner '{folder}' existiert nicht.")
        return

    print(f"Suche nach Dateien im Ordner: '{folder}'")

    files_renamed = 0

    # Durchsuche alle Dateien im angegebenen Ordner
    for filename in os.listdir(folder):
        # Wir wollen nur .jpg oder .jpeg Dateien bearbeiten
        if filename.lower().endswith(('.jpg', '.jpeg')):

            # Überprüfe, ob der Dateiname der Konvention '[vorname nachname]_...' entspricht
            if filename.startswith('[') and '_' in filename:

                # Finde das Ende des Namens-Teils, um Vor- und Nachnamen zu isolieren
                end_of_name_part = filename.find(']_')
                if end_of_name_part != -1:

                    # Extrahiere den Teil mit Vor- und Nachnamen
                    name_part = filename[1:end_of_name_part]

                    # Splitte den Namen in Teile am ersten Leerzeichen
                    parts = name_part.split(' ', 1)

                    # Überprüfe, ob wir mindestens zwei Teile haben (Vorname und Nachname)
                    if len(parts) == 2:
                        firstname = parts[0]
                        lastname = parts[1]

                        # Setze die Anfangsbuchstaben auf Großbuchstaben
                        capitalized_firstname = firstname.capitalize()
                        capitalized_lastname = lastname.capitalize()

                        # Setze den neuen Namensteil zusammen
                        new_name_part = f"{capitalized_firstname} {capitalized_lastname}"

                        # Erstelle den neuen, vollständigen Dateinamen
                        new_filename = filename.replace(name_part, new_name_part, 1)

                        # Zeige dem Benutzer die geplante Änderung
                        print(f"Ändere: '{filename}'")
                        print(f"   zu:   '{new_filename}'")

                        # Benenne die Datei um
                        old_path = os.path.join(folder, filename)
                        new_path = os.path.join(folder, new_filename)

                        try:
                            os.rename(old_path, new_path)
                            files_renamed += 1
                        except Exception as e:
                            print(f"Fehler beim Umbennen von '{filename}': {e}")

    print("\n---")
    print(f"Vorgang abgeschlossen. {files_renamed} Dateien wurden umbenannt.")


if __name__ == '__main__':
    rename_files(FOLDER_PATH)