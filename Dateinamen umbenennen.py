import os # Importiert das 'os'-Modul, das Funktionen für die Interaktion mit dem Betriebssystem bereitstellt.
           # Dies beinhaltet Operationen wie das Auflisten von Verzeichnissen, das Prüfen von Pfaden
           # und das Umbenennen von Dateien.

def rename_images_with_folder_name(base_path):
    """
    Benennt Bilddateien in einer spezifischen Ordnerstruktur um.

    Die Ordnerstruktur wird erwartet als:
    base_path (z.B. 'e:\\Bilder\\Celebrities\\')
    └── A-Z Ordner (z.B. 'A', 'B', 'C', ...)
        └── Personenordner (z.B. 'Bonnie Tyler', 'Brad Pitt', ...)
            └── Bilddateien (z.b. 'Konzert2017.jpg')

    Der neue Dateiname wird gebildet, indem der Name des 'Personenordners'
    in eckige Klammern vor den ursprünglichen Dateinamen gestellt und
    durch einen Unterstrich getrennt wird.
    Beispiel: 'Konzert2017.jpg' im Ordner 'Bonnie Tyler' wird zu '[Bonnie Tyler]_Konzert2017.jpg'.

    Args:
        base_path (str): Der absolute Basispfad, von dem aus die Operation gestartet werden soll.
                         Dies ist der Pfad zum 'Celebrities'-Ordner.
    """

    # --- Vorabprüfung des Basispfades ---
    if not os.path.isdir(base_path):
        # Prüft, ob der angegebene Basispfad tatsächlich existiert und ein Verzeichnis ist.
        # Wenn nicht, wird eine Fehlermeldung ausgegeben und die Funktion beendet.
        print(f"Fehler: Der Basispfad '{base_path}' existiert nicht oder ist kein Verzeichnis.")
        return # Beendet die Funktion vorzeitig.

    print(f"Starte Umbenennungsvorgang im Basispfad: {base_path}\n")

    # --- Konfiguration der erlaubten Bilddateierweiterungen ---
    # Definiert ein Tuple (eine unveränderliche Liste) von Dateierweiterungen,
    # die als Bilddateien betrachtet und umbenannt werden sollen.
    # Alle Erweiterungen werden in Kleinbuchstaben angegeben, um einen
    # case-insensitiven Vergleich zu ermöglichen.
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.avif')
    print(f"Es werden nur Dateien mit folgenden Erweiterungen verarbeitet: {', '.join(image_extensions)}\n")


    # --- Schritt 1: Iteration durch die A-Z Buchstaben-Ordner ---
    # os.listdir(base_path) gibt eine Liste aller Dateien und Unterverzeichnisse
    # im angegebenen 'base_path' zurück. Hier sind das die A-Z Ordner.
    for char_folder_name in sorted(os.listdir(base_path)): # 'sorted()' sorgt für eine alphabetische Reihenfolge.
        # Erstellt den vollständigen Pfad zum aktuellen Buchstaben-Ordner.
        char_folder_path = os.path.join(base_path, char_folder_name)

        # Überprüft, ob das aktuelle Element ein Verzeichnis ist UND
        # ob der Ordnername ein einzelner Buchstabe ist (optional, aber gut zur Validierung).
        if os.path.isdir(char_folder_path) and len(char_folder_name) == 1 and char_folder_name.isalpha():
            print(f"Betrete Buchstaben-Ordner: {char_folder_name}\\")

            # --- Schritt 2: Iteration durch die Personen-Ordner innerhalb des Buchstaben-Ordners ---
            # os.listdir(char_folder_path) gibt eine Liste aller Dateien und Unterverzeichnisse
            # im aktuellen Buchstaben-Ordner zurück. Hier sind das die Personen-Ordner.
            for person_folder_name in sorted(os.listdir(char_folder_path)): # 'sorted()' sorgt für eine alphabetische Reihenfolge.
                # Erstellt den vollständigen Pfad zum aktuellen Personen-Ordner.
                person_folder_path = os.path.join(char_folder_path, person_folder_name)

                # Überprüft, ob das aktuelle Element ein Verzeichnis ist (d.h., ein Personen-Ordner).
                if os.path.isdir(person_folder_path):
                    print(f"  Verarbeite Personen-Ordner: {person_folder_name}\\")

                    # --- Schritt 3: Iteration durch die Dateien im Personen-Ordner ---
                    # os.listdir(person_folder_path) gibt eine Liste aller Dateien
                    # im aktuellen Personen-Ordner zurück.
                    for filename in os.listdir(person_folder_path):
                        # Erstellt den vollständigen Pfad zur aktuellen Datei.
                        old_file_path = os.path.join(person_folder_path, filename)

                        # Überprüft, ob das aktuelle Element eine tatsächliche Datei ist (und kein Unterordner).
                        if os.path.isfile(old_file_path):
                            # os.path.splitext() teilt den Dateinamen in Basisname und Erweiterung auf.
                            # Beispiel: "Konzert2017.jpg" -> name="Konzert2017", extension=".jpg"
                            name, extension = os.path.splitext(filename)

                            # Konvertiert die Dateierweiterung in Kleinbuchstaben für den Vergleich.
                            # Beispiel: ".JPG" wird zu ".jpg"
                            if extension.lower() in image_extensions:
                                # Prüft, ob die Dateierweiterung in unserer vordefinierten Liste
                                # der erlaubten Bildformate enthalten ist.
                                # Nur wenn dies zutrifft, wird die Datei weiterverarbeitet.

                                # Überprüft, ob die Datei bereits das gewünschte Namensformat hat.
                                # Dies verhindert ein mehrfaches Umbenennen oder das Hinzufügen
                                # doppelter Präfixe, falls das Skript mehrmals ausgeführt wird.
                                if not filename.startswith(f"[{person_folder_name}]_"):
                                    # Erstellt den neuen Dateinamen gemäß der Spezifikation:
                                    # '[Personenordnername]_Originaldateiname.Originalerweiterung'
                                    new_filename = f"[{person_folder_name}]_{name}{extension}"
                                    # Erstellt den vollständigen Pfad zum neuen Dateinamen.
                                    new_file_path = os.path.join(person_folder_path, new_filename)

                                    try:
                                        # Führt die eigentliche Umbenennungsoperation durch.
                                        # os.rename() verschiebt oder benennt eine Datei um.
                                        os.rename(old_file_path, new_file_path)
                                        print(f"    Umbenannt: '{filename}' -> '{new_filename}'")
                                    except OSError as e:
                                        # Fängt mögliche Betriebssystemfehler ab, die während des Umbenennens auftreten können.
                                        # Dies könnte passieren, wenn die Datei gesperrt ist, Berechtigungen fehlen, etc.
                                        print(f"    Fehler beim Umbenennen von '{filename}': {e}")
                                else:
                                    # Wenn die Datei bereits das gewünschte Präfix hat, wird sie übersprungen.
                                    print(f"    Überspringe '{filename}' (bereits umbenannt oder ähnliches Format).")
                            else:
                                # Wenn die Dateierweiterung kein Bildformat ist, wird die Datei übersprungen.
                                print(f"    Überspringe '{filename}' (kein Bildformat).")
                        else:
                            # Wenn das Element im Personen-Ordner keine Datei ist (z.B. ein weiterer Unterordner),
                            # wird es übersprungen.
                            print(f"    Überspringe '{filename}' (keine Datei).")
                else:
                    # Wenn das Element im Buchstaben-Ordner kein Verzeichnis ist, wird es übersprungen.
                    print(f"  Überspringe '{person_folder_name}' (kein Verzeichnis).")
        else:
            # Wenn das Element im Basispfad kein einzelner Buchstaben-Ordner ist, wird es übersprungen.
            print(f"Überspringe '{char_folder_name}' (kein einzelner Buchstaben-Ordner oder Verzeichnis).")

    print("\nUmbenennungsvorgang abgeschlossen.")


# --- Verwendung des Skripts ---
if __name__ == "__main__":
    # Dieser Block wird nur ausgeführt, wenn das Skript direkt gestartet wird (nicht, wenn es importiert wird).

    # Definiere den Basispfad zu deinem 'Celebrities'-Ordner.
    # WICHTIG: Verwende einen "Raw String" (beginnt mit 'r'), um Probleme mit Backslashes ('\')
    #          als Escape-Zeichen in Windows-Pfaden zu vermeiden.
    # Alternativ könnten doppelte Backslashes ('\\') verwendet werden: 'e:\\Bilder\\Celebrities'
    base_directory = r'd:\RedditDownloads\reddit_sub_GermanCelebs'

    # --- SICHERHEITSHINWEIS ---
    # Dieses Skript nimmt permanente Änderungen an deinen Dateinamen vor.
    # Es wird DRINGEND empfohlen, VOR der Ausführung dieses Skripts eine
    # VOLLSTÄNDIGE SICHERUNGSKOPIE deiner Daten zu erstellen.
    # Alternativ kannst du das Skript zuerst in einem kleinen, dedizierten
    # Testordner mit Dummy-Dateien ausprobieren.

    # Ruft die Hauptfunktion auf, um den Umbenennungsprozess zu starten.
    rename_images_with_folder_name(base_directory)