# ==============================================================================
# Dateiname Vorschlag (Deutsch): dateiendung_korrigieren.py
# Dateiname Vorschlag (Technisch): file_extension_validator.py
#
# Beschreibung: Dieses Skript durchsucht rekursiv ein Verzeichnis (ROOT_FOLDER)
#               nach Mediendateien (Bilder/Videos). Es verwendet das externe Modul
#               'filetype', um den tatsächlichen Dateityp (Magic Number) zu
#               ermitteln, unabhängig von der aktuellen Dateierweiterung.
#               Wenn die gefundene korrekte Endung (z.B. 'jpeg') nicht mit der
#               vorhandenen Endung (z.B. 'png') übereinstimmt, wird die Datei
#               umbenannt, um die korrekte Erweiterung zu verwenden.
#               Dies ist besonders nützlich, um Dateibeschädigungen oder falsche
#               Downloads zu bereinigen.
# ==============================================================================

import os
import filetype  # Benötigt: pip install filetype

# Konfigurieren des zu durchsuchenden Ordners
# Ändern Sie diesen Pfad, wenn Ihr Ordner woanders liegt
ROOT_FOLDER = r"d:\extracted\rips"


def get_real_extension(filepath):
    """
    Bestimmt die korrekte Dateierweiterung basierend auf dem tatsächlichen
    Dateityp ('Magic Number') der Datei.
    """
    try:
        # Ermittelt den Dateityp der Datei
        kind = filetype.guess(filepath)
        if kind is not None:
            # Gibt die korrekte Erweiterung als Kleinbuchstaben zurück (z.B. 'jpg' oder 'mp4')
            return kind.extension
        # Gibt None zurück, wenn der Typ nicht erkannt wird
        return None
    except Exception as e:
        print(f"Fehler beim Ermitteln des Dateityps für {os.path.basename(filepath)}: {e}")
        return None


def rename_file(filepath, new_extension):
    """
    Benennt die Datei um, falls die aktuelle Endung nicht mit dem tatsächlichen
    Dateityp übereinstimmt.
    """
    # Teilt den Pfad in Namen und aktuelle Endung
    current_name, current_extension = os.path.splitext(filepath)
    # Entfernt den führenden Punkt
    current_extension = current_extension.lstrip('.')

    # Überprüfung auf Abweichung zwischen aktueller und korrekter Endung
    if current_extension.lower() != new_extension.lower():
        # Konstruiert den neuen Dateipfad
        new_filepath = f"{current_name}.{new_extension}"

        # Benennt die Datei um
        try:
            # Sicherheitsprüfung: Existiert die Zieldatei bereits?
            if os.path.exists(new_filepath):
                print(
                    f"WARNUNG: Umbenennung von '{os.path.basename(filepath)}' fehlgeschlagen. Ziel '{os.path.basename(new_filepath)}' existiert bereits.")
                return False

            os.rename(filepath, new_filepath)
            print(f"✅ Umbenannt: '{os.path.basename(filepath)}' -> '{os.path.basename(new_filepath)}'")
            return True
        except Exception as e:
            print(f"❌ FEHLER beim Umbenennen von '{os.path.basename(filepath)}': {e}")
            return False

    # Gibt False zurück, wenn keine Umbenennung nötig war
    return False


def main():
    """
    Hauptfunktion, die den Ordner durchläuft und Dateien verarbeitet.
    """
    # Überprüft, ob der Ordner existiert
    if not os.path.isdir(ROOT_FOLDER):
        print(f"Fehler: Der angegebene Ordner '{ROOT_FOLDER}' existiert nicht.")
        return

    print(f"Starte die Überprüfung und Korrektur der Dateierweiterungen in '{ROOT_FOLDER}'...")
    renamed_count = 0
    checked_count = 0

    # Liste der Dateiendungen, die überhaupt geprüft werden sollen (Filter)
    # Beinhaltet gängige Bild- und Videoformate
    extensions_to_check = ('.jpg', '.jpeg', '.gif', '.png', '.bmp', '.mp4', '.mov', '.webp', '.tif', '.tiff')

    # Durchläuft den Ordner und alle Unterordner (rekursiv)
    # KORREKTUR für ValueError: os.walk gibt immer 3 Werte zurück: dirpath, dirnames, filenames
    for dirpath, dirnames, filenames in os.walk(ROOT_FOLDER):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            # Überprüft, ob die Datei eine der Endungen hat, die wir prüfen wollen
            if not any(filename.lower().endswith(ext) for ext in extensions_to_check):
                continue

            checked_count += 1
            real_extension = get_real_extension(filepath)

            if real_extension:
                # Versucht die Umbenennung, wenn eine Diskrepanz besteht
                if rename_file(filepath, real_extension):
                    renamed_count += 1
            else:
                # KORREKTUR für IndentationError: 'pass' muss aktiv sein, um einen leeren Block zu definieren
                # Optional: Protokollierung von Dateien, deren Typ nicht ermittelt werden konnte
                pass

    print("-" * 50)
    print("Überprüfung abgeschlossen.")
    print(f"Insgesamt {checked_count} Dateien auf Erweiterungsfehler geprüft.")
    print(f"Anzahl umbenannter Dateien: {renamed_count}")
    print("-" * 50)


if __name__ == "__main__":
    main()