# ==============================================================================
# Dateiname Vorschlag (Deutsch): laengster_dateiname_finden.py
# Dateiname Vorschlag (Technisch): longest_filename_finder.py
#
# Beschreibung: Dieses Skript durchsucht rekursiv alle Ordner eines angegebenen
#               Laufwerks (oder Verzeichnisses). Es identifiziert die Datei,
#               deren reiner Name (ohne Pfadangaben) die höchste Anzahl von
#               Zeichen aufweist. Es gibt den vollständigen Pfad zu dieser
#               Datei und die Länge des Dateinamens zurück.
# ==============================================================================

import os


def finde_laengste_datei(laufwerk):
    """
    Durchsucht das angegebene Laufwerk rekursiv und findet die Datei
    mit dem längsten reinen Dateinamen.

    Gibt den vollständigen Pfad und die Länge des Dateinamens zurück.
    """
    laengste_datei = ""
    # Speichert die Länge des längsten Dateinamens, der bisher gefunden wurde
    laengste_dateiname_laenge = 0
    # Speichert die Anzahl der durchsuchten Dateien
    datei_zaehler = 0

    print(f"Starte Suche nach dem längsten Dateinamen in: '{laufwerk}'")

    if not os.path.exists(laufwerk):
        print(f"❌ Fehler: Das Laufwerk/Verzeichnis '{laufwerk}' wurde nicht gefunden.")
        return None, 0

    # os.walk durchläuft das Verzeichnis rekursiv
    for ordnername, unterordner, dateinamen in os.walk(laufwerk):
        for dateiname in dateinamen:
            datei_zaehler += 1
            # Berechnet die Länge des reinen Dateinamens (z.B. "dokument.pdf")
            dateiname_laenge = len(dateiname)

            # Prüft, ob der aktuelle Name länger ist als der bisher längste
            if dateiname_laenge > laengste_dateiname_laenge:
                laengste_dateiname_laenge = dateiname_laenge
                laengste_datei = os.path.join(ordnername, dateiname)
                # print(f"-> Neuer längster Name gefunden: {dateiname} ({dateiname_laenge} Zeichen)") # Optionales Debugging

    if laengste_datei:
        # Die Rückgabe beinhaltet den vollständigen Pfad und die Länge des Dateinamens
        return laengste_datei, laengste_dateiname_laenge, datei_zaehler
    else:
        return None, 0, datei_zaehler


if __name__ == "__main__":
    # Hier bitte den Laufwerksbuchstaben oder Pfad anpassen
    laufwerk = "e:\\"

    # Fügt eine Fehlerbehandlung hinzu, falls os.walk fehlschlägt (z.B. bei Zugriffsproblemen)
    try:
        laengste_datei, laenge, anzahl = finde_laengste_datei(laufwerk)
    except Exception as e:
        print(f"❌ Ein unerwarteter Fehler während der Suche ist aufgetreten: {e}")
        laengste_datei, laenge, anzahl = None, 0, 0

    print("\n" + "=" * 50)
    print("--- Suche abgeschlossen ---")

    if laengste_datei:
        # Extrahiert den reinen Dateinamen für eine klarere Ausgabe
        reiner_name = os.path.basename(laengste_datei)

        print(f"✅ Die Datei mit dem längsten Dateinamen ist:")
        print(f"   Name: **{reiner_name}**")
        print(f"   Länge: **{laenge}** Zeichen")
        print(f"   Pfad: {laengste_datei}")
        print(f"   Insgesamt {anzahl} Dateien durchsucht.")
    else:
        if anzahl > 0:
            print(f"Keine Datei gefunden, die das Kriterium erfüllt hätte (es wurden {anzahl} Objekte durchsucht).")
        else:
            print("Keine Dateien im angegebenen Laufwerk gefunden.")
    print("=" * 50)