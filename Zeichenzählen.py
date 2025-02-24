import os

def finde_laengste_datei(laufwerk):
    laengste_datei = ""
    laengste_dateiname_laenge = 0

    for ordnername, unterordner, dateinamen in os.walk(laufwerk):
        for dateiname in dateinamen:
            dateiname_laenge = len(dateiname)
            if dateiname_laenge > laengste_dateiname_laenge:
                laengste_dateiname_laenge = dateiname_laenge
                laengste_datei = os.path.join(ordnername, dateiname)

    if laengste_datei:
        return laengste_datei, laengste_dateiname_laenge
    else:
        return None, 0

if __name__ == "__main__":
    laufwerk = "k:\\"  # Hier bitte den Laufwerksbuchstaben anpassen
    laengste_datei, laenge = finde_laengste_datei(laufwerk)

    if laengste_datei:
        print("Die Datei mit dem längsten Dateinamen ist:", laengste_datei)
        print("Der Dateiname ist", laenge, "Zeichen lang.")
    else:
        print("Keine Dateien im angegebenen Laufwerk gefunden.")