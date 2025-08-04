import os # Importiert das 'os'-Modul, das Funktionen für die Interaktion mit dem Betriebssystem bereitstellt.

def rename_images_with_folder_name(base_path):
    """
    Benennt Bilddateien in einer spezifischen Ordnerstruktur um.

    Die Ordnerstruktur wird erwartet als:
    base_path (z.B. 'e:\\Bilder\\Celebrities\\V\\Vintage\\')
    └── Playboy-Modell Ordner (z.B. 'Peggy Sue', 'Betty Page', ...)
        └── Bilddateien (z.b. '1.jpg', 'Fotoshooting.png')

    Der neue Dateiname wird gebildet, indem der Name des 'Playboy-Modell Ordners'
    in eckige Klammern vor den ursprünglichen Dateinamen gestellt und
    durch einen Unterstrich getrennt wird.
    Beispiel: '1.jpg' im Ordner 'Peggy Sue' wird zu '[Peggy Sue]_1.jpg'.

    Args:
        base_path (str): Der absolute Basispfad, von dem aus die Operation gestartet werden soll.
                         Dies ist der Pfad zum 'Vintage'-Ordner.
    """

    # --- Vorabprüfung des Basispfades ---
    if not os.path.isdir(base_path):
        print(f"Fehler: Der Basispfad '{base_path}' existiert nicht oder ist kein Verzeichnis.")
        return

    print(f"Starte Umbenennungsvorgang im Basispfad: {base_path}\n")

    # --- Konfiguration der erlaubten Bilddateierweiterungen ---
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.avif')
    print(f"Es werden nur Dateien mit folgenden Erweiterungen verarbeitet: {', '.join(image_extensions)}\n")


    # --- Schritt 1: Iteration durch die Playboy-Modell Ordner ---
    # os.listdir(base_path) gibt eine Liste aller Dateien und Unterverzeichnisse
    # im angegebenen 'base_path' zurück. Hier sind das die Modell-Ordner.
    for model_folder_name in sorted(os.listdir(base_path)): # 'sorted()' sorgt für eine alphabetische Reihenfolge.
        # Erstellt den vollständigen Pfad zum aktuellen Modell-Ordner.
        model_folder_path = os.path.join(base_path, model_folder_name)

        # Überprüft, ob das aktuelle Element ein Verzeichnis ist (d.h., ein Modell-Ordner).
        if os.path.isdir(model_folder_path):
            print(f"Verarbeite Modell-Ordner: {model_folder_name}\\")

            # --- Schritt 2: Iteration durch die Dateien im Modell-Ordner ---
            # os.listdir(model_folder_path) gibt eine Liste aller Dateien
            # im aktuellen Modell-Ordner zurück.
            for filename in os.listdir(model_folder_path):
                # Erstellt den vollständigen Pfad zur aktuellen Datei.
                old_file_path = os.path.join(model_folder_path, filename)

                # Überprüft, ob das aktuelle Element eine tatsächliche Datei ist (und kein Unterordner).
                if os.path.isfile(old_file_path):
                    name, extension = os.path.splitext(filename)

                    if extension.lower() in image_extensions:
                        # Prüft, ob die Datei bereits das gewünschte Namensformat hat.
                        if not filename.startswith(f"[{model_folder_name}]_"):
                            # Erstellt den neuen Dateinamen gemäß der Spezifikation:
                            # '[Modellordnername]_Originaldateiname.Originalerweiterung'
                            new_filename = f"[{model_folder_name}]_{name}{extension}"
                            new_file_path = os.path.join(model_folder_path, new_filename)

                            try:
                                os.rename(old_file_path, new_file_path)
                                print(f"  Umbenannt: '{filename}' -> '{new_filename}'")
                            except OSError as e:
                                print(f"  Fehler beim Umbenennen von '{filename}': {e}")
                        else:
                            print(f"  Überspringe '{filename}' (bereits umbenannt oder ähnliches Format).")
                    else:
                        print(f"  Überspringe '{filename}' (kein Bildformat).")
                else:
                    print(f"  Überspringe '{filename}' (keine Datei).")
        else:
            print(f"Überspringe '{model_folder_name}' (kein Verzeichnis).")

    print("\nUmbenennungsvorgang abgeschlossen.")


# --- Verwendung des Skripts ---
if __name__ == "__main__":
    # Definiere den Basispfad zu deinem 'Vintage'-Ordner.
    base_directory = r'e:\Bilder\Celebrities' # Ohne abschließenden Backslash
    # --- SICHERHEITSHINWEIS ---
    # Dieses Skript nimmt permanente Änderungen an deinen Dateinamen vor.
    # Es wird DRINGEND empfohlen, VOR der Ausführung dieses Skripts eine
    # VOLLSTÄNDIGE SICHERUNGSKOPIE deiner Daten zu erstellen.
    # Alternativ kannst du das Skript zuerst in einem kleinen, dedizierten
    # Testordner mit Dummy-Dateien ausprobieren.

    # Ruft die Hauptfunktion auf, um den Umbenennungsprozess zu starten.
    rename_images_with_folder_name(base_directory)