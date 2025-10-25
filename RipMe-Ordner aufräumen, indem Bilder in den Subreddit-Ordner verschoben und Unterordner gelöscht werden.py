import os
import shutil

# --- Konfiguration ---
HAUPT_ORDNER = r'd:\extracted\rips'

# Die Korrektur ist hier: '\\?\\' statt '\\?\'
# Der Windows Long Path Prefix, um die 260-Zeichen-Grenze zu umgehen
WINDOWS_LONG_PATH_PREFIX = r'\\?\\'


def get_long_path(path):
    """Fügt das erweiterte Pfadpräfix für Windows hinzu, wenn es fehlt."""
    # os.path.abspath wandelt den Pfad in einen absoluten Pfad um
    abs_path = os.path.abspath(path)

    # Prüfen, ob das Präfix bereits vorhanden ist, um Duplikate zu vermeiden
    if abs_path.startswith(WINDOWS_LONG_PATH_PREFIX):
        return abs_path

    # Für Pfade auf Laufwerken wie 'd:\' wird das Präfix nach dem Laufwerksbuchstaben eingefügt
    # (z.B. \\?\D:\RedditDownloads)
    if os.path.splitdrive(abs_path)[0]:
        # Wichtig: Wir fügen das Präfix \\?\ dem Pfad ohne das Laufwerks-Backslash hinzu
        return WINDOWS_LONG_PATH_PREFIX + abs_path.lstrip('\\')

    return abs_path  # Rückgabe des Pfades, falls es kein Windows-Pfad ist


# --- Funktion zur Bereinigung ---
def entschachteln_und_bereinigen(hauptpfad):
    """
    Durchsucht den Hauptordner, verschiebt Dateien aus verschachtelten
    Unterordnern und löscht leere Ordner, während Pfadlängenfehler ignoriert werden.
    """
    print(f"Starte Bereinigung im Hauptordner: {hauptpfad}")

    # Zähler für die Übersicht
    verschobene_dateien = 0
    geloeschte_ordner = 0
    uebersprungene_fehler = 0

    # os.walk(..., topdown=False) ist wichtig für die Löschung von innen nach außen
    for root, dirs, files in os.walk(hauptpfad, topdown=False):

        # Ignoriere den Hauptordner selbst und Ordner, die noch Unterordner enthalten
        if root == hauptpfad or dirs:
            continue

        # **********************************************
        # Das ist der Pfad zum **Thread-Ordner** (z.B. "Bea die Kurven Queen")
        thread_pfad = root

        # Der übergeordnete Ordner ist der **Subreddit-Ordner**
        subreddit_pfad = os.path.dirname(thread_pfad)

        # Verhindern, dass der Hauptordner selbst Zielort ist
        if subreddit_pfad == hauptpfad:
            continue
        # **********************************************

        # 1. Verschiebe alle Dateien aus dem Thread-Ordner in den Subreddit-Ordner
        dateien_im_thread = os.listdir(thread_pfad)

        print(f"\n-> Bearbeite Ordner: {thread_pfad}")

        for datei_name in dateien_im_thread:
            alte_datei_pfad_normal = os.path.join(thread_pfad, datei_name)
            neue_datei_pfad_normal = os.path.join(subreddit_pfad, datei_name)

            # WICHTIG: Anwendung des Long Path Präfixes für die Operationen
            # Wir verwenden die normalen Pfade für os.path.isfile, da es stabiler ist
            if os.path.isfile(alte_datei_pfad_normal):

                # Jetzt Long Path für die kritische Move-Operation abrufen
                alte_datei_pfad = get_long_path(alte_datei_pfad_normal)
                neue_datei_pfad = get_long_path(neue_datei_pfad_normal)

                try:
                    # Verschieben der Datei
                    shutil.move(alte_datei_pfad, neue_datei_pfad)
                    verschobene_dateien += 1
                    print(f"   [Verschoben]: {datei_name}")

                # Fängt allgemeine Fehler ab, einschließlich 'Path Too Long', 'Access Denied' oder Duplikate
                except (OSError, PermissionError, shutil.Error) as e:
                    uebersprungene_fehler += 1
                    print(f"   [FEHLER/ÜBERSPRUNGEN]: Konnte '{datei_name}' nicht verschieben. {type(e).__name__}: {e}")

        # 2. Versuch, den Thread-Ordner zu löschen
        thread_pfad_lang = get_long_path(thread_pfad)
        try:
            # os.rmdir löscht nur leere Verzeichnisse
            os.rmdir(thread_pfad_lang)
            geloeschte_ordner += 1
            print(f"<- Ordner erfolgreich gelöscht: {os.path.basename(thread_pfad)}")
        except (OSError, PermissionError) as e:
            # Ordner nicht leer, Pfadlänge oder Berechtigungsproblem
            uebersprungene_fehler += 1
            print(
                f"  [NICHT GELÖSCHT] Ordner '{os.path.basename(thread_pfad)}' ist nicht leer oder konnte nicht gelöscht werden. {type(e).__name__}: {e}")

    # --- Zusammenfassung ---
    print("\n" + "=" * 70)
    print("ZUSAMMENFASSUNG DER BEREINIGUNG")
    print(f"Gesamt verschobene Dateien: {verschobene_dateien}")
    print(f"Gelöschte leere Ordner: {geloeschte_ordner}")
    print(f"Übersprungene Fehler (Pfadlänge/Zugriff/Duplikat): {uebersprungene_fehler}")
    print("=" * 70)


# --- Ausführung ---
if __name__ == '__main__':
    entschachteln_und_bereinigen(HAUPT_ORDNER)