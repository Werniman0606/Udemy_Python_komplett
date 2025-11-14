# ==============================================================================
# Dateiname Vorschlag (Deutsch): dateiname_namen_titel_formatieren_korrigiert.py
# Dateiname Vorschlag (Technisch): filename_capitalize_prefix_v2.py
#
# Beschreibung: KORRIGIERTE VERSION. Behebt den Fehler bei Komma-getrennten
#               Namen, indem jeder Name (Vorname Nachname) einzeln im Title-Case
#               formatiert wird, um z.B. '[Sarah Reichow, Sven Reichow]'
#               korrekt zu erhalten.
# ==============================================================================

import os

# --- KONFIGURATION START ---
FOLDER_PATH = r'e:\Bilder'


# --- KONFIGURATION ENDE ---

def special_capitalize_name(full_name_part):
    """
    Formatiert einen einzelnen Namensteil (Vorname Nachname) korrekt in Title Case.
    """
    # Trimme Leerzeichen vor und nach dem Namen
    full_name_part = full_name_part.strip()

    # Splitte am ersten Leerzeichen (Vorname und Nachname trennen)
    parts = full_name_part.split(' ', 1)

    if len(parts) < 2:
        # Dies ist ein einzelner Name oder hat keine Leerzeichen (z.B. 'sarah')
        # Verwende .title(), um auch Namen mit Bindestrich ('Marie-louise') zu behandeln.
        return full_name_part.title()

    firstname = parts[0]
    lastname_with_parts = parts[1]  # Der Rest

    # Capitalize() für Vorname und Title() für Nachname (um Bindestriche zu behandeln)
    # Wichtig: Wir splitten den Nachnamen nicht weiter, da er möglicherweise Namenszusätze enthält.

    # Bessere Methode, um auch Bindestriche zu behandeln:
    # Wir wenden .title() auf den gesamten Namen an, da es in diesem Kontext am robustesten ist.
    # Wenn wir annehmen, dass Namen wie "Sarah-Reichow" korrekt formatiert werden sollen.

    # Hier der Kompromiss: Wir wissen, dass es Vor- und Nachname sind, also splitten wir.
    # Wir nutzen eine einfache, aber effektive Methode:

    formatted_firstname = firstname.capitalize()

    # Für den Nachnamensteil verwenden wir Title(), um z.B. 'von' oder 'd' 's' korrekt zu behandeln.
    # Bei 'reichow' ist capitalize() ausreichend, aber title() bietet mehr Schutz für 'van der'.
    formatted_lastname = lastname_with_parts.title()

    return f"{formatted_firstname} {formatted_lastname}"


def rename_files(folder):
    """
    Durchsucht einen Ordner und benennt Dateien um, korrigiert die Schreibweise
    von Komma-getrennten Namen im Präfix.
    """
    if not os.path.isdir(folder):
        print(f"Fehler: Der angegebene Ordner '{folder}' existiert nicht.")
        return

    print(f"Suche nach Dateien im Ordner: '{folder}'")

    files_renamed = 0

    # Durchsuche alle Dateien im angegebenen Ordner
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.jpg', '.jpeg')):

            if filename.startswith('[') and '_' in filename:

                end_of_name_part = filename.find(']_')
                if end_of_name_part != -1:

                    # Extrahiere den Teil mit Vor- und Nachnamen (z.B. 'sarah reichow, sven reichow')
                    name_part_lower = filename[1:end_of_name_part]

                    # --- KORRIGIERTE LOGIK START ---

                    # 1. Teile die Liste in einzelne Namen an den Kommas.
                    individual_names = [name.strip() for name in name_part_lower.split(',')]

                    formatted_names = []

                    # 2. Formatiere jeden einzelnen Namen (Vorname Nachname) mit der Hilfsfunktion.
                    for name in individual_names:
                        formatted_name = special_capitalize_name(name)
                        formatted_names.append(formatted_name)

                    # 3. Füge die formatierten Namen wieder mit Komma und Leerzeichen zusammen.
                    new_name_part = ", ".join(formatted_names)

                    # --- KORRIGIERTE LOGIK ENDE ---

                    # Prüfen, ob eine Änderung überhaupt notwendig ist
                    if name_part_lower == new_name_part.lower():
                        continue

                    # Erstelle den neuen, vollständigen Dateinamen
                    # Ersetze nur das erste Vorkommen (das ist der Präfix)
                    new_filename = filename.replace(name_part_lower, new_name_part, 1)

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