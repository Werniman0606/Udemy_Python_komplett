# ==============================================================================
# Dateiname Vorschlag (Deutsch): laengster_dateiname_alle_laufwerke.py
# Dateiname Vorschlag (Technisch): longest_filename_all_drives.py
#
# Beschreibung: Dieses Skript durchsucht rekursiv alle gefundenen lokalen Laufwerke
#               von C: bis Z: und findet die Datei, deren reiner Dateiname (ohne
#               Pfad) die höchste Zeichenanzahl aufweist.
# ==============================================================================

import os
import string
import sys

# Fügt das erweiterte Pfadpräfix für Windows hinzu, um Pfade über 260 Zeichen
# für os.walk zugänglich zu machen (wichtig bei Tiefensuche).
WINDOWS_LONG_PATH_PREFIX = r'\\?\\'


def get_long_path(path):
    """Fügt das erweiterte Pfadpräfix für Windows hinzu."""
    abs_path = os.path.abspath(path)
    if os.path.splitdrive(abs_path)[0]:
        return WINDOWS_LONG_PATH_PREFIX + abs_path
    return abs_path


def finde_laengste_datei(laufwerk):
    """
    Durchsucht das angegebene Laufwerk rekursiv und findet die Datei
    mit dem längsten reinen Dateinamen. Gibt den Pfad, die Länge des
    Dateinamens und die Anzahl der durchsuchten Dateien zurück.
    """
    laengste_datei = None
    laengste_dateiname_laenge = 0
    datei_zaehler = 0

    # Nutze get_long_path, um das Laufwerk zu öffnen und Pfadlimit-Fehler zu vermeiden
    start_pfad = get_long_path(laufwerk)

    # os.walk durchläuft das Verzeichnis rekursiv
    try:
        for ordnername, unterordner, dateinamen in os.walk(start_pfad):
            for dateiname in dateinamen:
                datei_zaehler += 1

                # Wir berechnen die Länge des reinen Dateinamens
                dateiname_laenge = len(dateiname)

                if dateiname_laenge > laengste_dateiname_laenge:
                    laengste_dateiname_laenge = dateiname_laenge

                    # Wichtig: Speichere den Pfad ohne das Long Path Präfix für die Ausgabe
                    if ordnername.startswith(WINDOWS_LONG_PATH_PREFIX):
                        # Entfernt das \\?\ und das Laufwerksschema (z.B. C:\)
                        # und fügt den Dateinamen an
                        laengste_datei = os.path.join(ordnername[4:], dateiname)
                    else:
                        laengste_datei = os.path.join(ordnername, dateiname)

    except Exception as e:
        # Fängt Fehler bei nicht verfügbaren Laufwerken, Berechtigungen usw. ab
        print(f"⚠️ FEHLER bei der Suche auf '{laufwerk}': {e}")
        # Gibt die bisherigen Ergebnisse dieses Laufwerks zurück, falls der Fehler früh auftrat
        return laengste_datei, laengste_dateiname_laenge, datei_zaehler

    return laengste_datei, laengste_dateiname_laenge, datei_zaehler


def main():
    """
    Hauptfunktion: Durchläuft alle möglichen Laufwerksbuchstaben und kombiniert die Ergebnisse.
    """
    global_laengste_datei = None
    global_laengste_laenge = 0
    global_anzahl = 0

    print("Starte die Suche nach dem längsten Dateinamen auf allen lokalen Laufwerken (C: bis Z:).")

    # Durchläuft alle Großbuchstaben von C bis Z
    for buchstabe in string.ascii_uppercase[2:]:
        laufwerk = f"{buchstabe}:\\"

        # Prüfen, ob das Laufwerk existiert und zugänglich ist
        if os.path.exists(laufwerk):
            print(f"\n--- Prüfe Laufwerk: {laufwerk} ---")

            # Führe die Suche auf dem aktuellen Laufwerk aus
            datei, laenge, anzahl = finde_laengste_datei(laufwerk)
            global_anzahl += anzahl

            if datei and laenge > global_laengste_laenge:
                global_laengste_laenge = laenge
                global_laengste_datei = datei
                print(f"-> Neuer globaler Rekord: '{os.path.basename(datei)}' ({laenge} Zeichen)")

        # else: Laufwerk nicht gefunden/aktiv/existiert nicht (z.B. leeres CD-Laufwerk)

    print("\n" + "=" * 60)
    print("--- ZUSAMMENFASSUNG DER GLOBALEN SUCHE ---")

    if global_laengste_datei:
        reiner_name = os.path.basename(global_laengste_datei)

        print(f"✅ Die Datei mit dem **längsten Dateinamen** ist:")
        print(f"   Name: **{reiner_name}**")
        print(f"   Länge: **{global_laengste_laenge}** Zeichen")
        print(f"   Pfad: {global_laengste_datei}")
        print(f"   Insgesamt {global_anzahl} Dateien durchsucht.")
    else:
        print("Keine Dateien auf den geprüften Laufwerken gefunden.")
    print("=" * 60)


if __name__ == "__main__":
    main()