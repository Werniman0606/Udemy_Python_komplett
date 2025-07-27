import os # Importiert das 'os'-Modul für Betriebssystem-Interaktionen

def organize_celebrity_images(base_path):
    """
    Verschiebt Bild- und Videodateien, die sich direkt im Basispfad befinden und einem spezifischen
    Namensschema entsprechen, in ihre korrekten Unterordner.
    Dabei werden bei Bedarf Buchstaben- und Personenordner erstellt.

    Erwartetes Namensschema der zu verschiebenden Dateien: '[Personenname]_Originaldateiname.Erweiterung'
    Beispiel: '[Amy Lee]_Anette Olzon.jpg', '[John Doe]_Clip.mp4'

    Zielordnerstruktur:
    base_path (z.B. 'e:\\Bilder\\Celebrities\\')
    └── A-Z Ordner (z.B. 'A', 'B', 'C', ...)
        └── Personenordner (z.B. 'Amy Lee', 'Brad Pitt', ...)
            └── Verschobene Datei

    Args:
        base_path (str): Der absolute Basispfad, z.B. 'e:\\Bilder\\Celebrities'.
    """

    if not os.path.isdir(base_path):
        print(f"Fehler: Der Basispfad '{base_path}' existiert nicht oder ist kein Verzeichnis.")
        return

    print(f"Starte Organisation von Dateien im Basispfad: {base_path}\n")

    # Konfiguration der erlaubten Dateierweiterungen (jetzt auch für Videos)
    # Hinzugefügt: .gif und .mp4
    allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.avif', '.mp4')
    print(f"Es werden nur Dateien mit folgenden Erweiterungen verarbeitet: {', '.join(allowed_extensions)}\n")

    # --- Schritt 1: Dateien direkt im Basispfad verarbeiten ---
    print(f"Suche nach Dateien zum Verschieben in: {base_path}\\")
    for filename in os.listdir(base_path):
        old_file_path = os.path.join(base_path, filename)

        if os.path.isfile(old_file_path):
            name, extension = os.path.splitext(filename)

            # Überprüfung gegen die erweiterte Liste der erlaubten Erweiterungen
            if extension.lower() in allowed_extensions:
                # Prüfen, ob die Datei dem Muster '[Personenname]_' entspricht
                # Das Muster beginnt mit '[' und endet mit ']_'
                if filename.startswith('[') and ']_' in filename:
                    try:
                        # Den Personennamen aus dem Dateinamen extrahieren
                        # Beispiel: '[Amy Lee]_Anette Olzon.jpg' -> 'Amy Lee'
                        person_name_end_index = filename.find(']_')
                        if person_name_end_index != -1:
                            person_folder_name = filename[1:person_name_end_index] # Von nach '[' bis vor ']_'
                            # Den ersten Buchstaben des Personennamens als Buchstaben-Ordner verwenden
                            char_folder_name = person_folder_name[0].upper()

                            # Zielpfad erstellen: base_path/Buchstabenordner/Personenordner/Dateiname
                            char_folder_path = os.path.join(base_path, char_folder_name)
                            person_folder_path = os.path.join(char_folder_path, person_folder_name)
                            new_file_path = os.path.join(person_folder_path, filename)

                            # Überprüfen und Erstellen des Buchstaben-Ordners
                            if not os.path.exists(char_folder_path):
                                print(f"  Erstelle Buchstaben-Ordner: {char_folder_path}\\")
                                os.makedirs(char_folder_path)

                            # Überprüfen und Erstellen des Personen-Ordners
                            if not os.path.exists(person_folder_path):
                                print(f"  Erstelle Personen-Ordner: {person_folder_path}\\")
                                os.makedirs(person_folder_path)

                            # Datei verschieben
                            if not os.path.exists(new_file_path): # Nur verschieben, wenn Zieldatei noch nicht existiert
                                os.rename(old_file_path, new_file_path)
                                print(f"  Verschoben: '{filename}' nach '{new_file_path}'")
                            else:
                                print(f"  Überspringe '{filename}': Zieldatei '{new_file_path}' existiert bereits.")
                        else:
                            print(f"  Überspringe '{filename}': Ungültiges Namensformat im Basispfad.")
                    except OSError as e:
                        print(f"  Fehler beim Verschieben von '{filename}': {e}")
                else:
                    print(f"  Überspringe '{filename}' im Basispfad (entspricht nicht dem '[Name]_'-Muster).")
            else:
                print(f"  Überspringe '{filename}' im Basispfad (kein unterstütztes Dateiformat).")
        else:
            print(f"  Überspringe '{filename}' im Basispfad (keine Datei).")

    print("\nOrganisation von Dateien im Basispfad abgeschlossen.")


# --- Verwendung des Skripts ---
if __name__ == "__main__":
    base_directory = r'e:\Bilder\Celebrities'

    # --- SICHERHEITSHINWEIS ---
    # Dieses Skript nimmt permanente Änderungen an deinen Dateinamen und Dateipfaden vor.
    # Es wird DRINGEND empfohlen, VOR der Ausführung dieses Skripts eine
    # VOLLSTÄNDIGE SICHERUNGSKOPIE deiner Daten zu erstellen.
    # Alternativ kannst du das Skript zuerst in einem kleinen, dedizierten
    # Testordner mit Dummy-Dateien ausprobieren.

    organize_celebrity_images(base_directory)