"""Aufgabe: Lese die Datei names.csv ein und berechne, welcher Name insgesamt in den USA am häufigsten vergeben wurde
Tips:
Lese zuerst die Daten in ein Dictionary ein und zähle, wie oft jeder Vorname insgesamt vorgekommen list
Analysiere erst dann das Dictionary und finde den häufigsten Vornamen heraus
Achte darauf,wenn du 2 Zahlen addieren möchtest, ggf. musst du einen String erst in eine Zahl wandeln
Schreibe den gesamten Code, der die Datei öffnet und durchgeht in eine Zelle"""


with open("names.csv","r") as file:
    names = {} # ein leeres Dictionary wird erstellt
    for line in file:
        splitted = (line.strip().split(",")) # aus der eingelesenen Zeile wird eine Liste namens spliited gemacht
        if splitted[0] == "Id": #wenn der erste Eintrag der Liste ID ist,
            continue #wird dieser Datensatz übersprungen,weil es sich dann um die Kopfzeile handelt,die wir nicht
            # brauchen
        # wir wissen,dass in den einzelnen Zeilen in der csv immer der Name an 2.Stelle und die Häufigkeit an
        # 6.Stelle steht. Diese kopieren wir jeweils in eine eigene Variable
        name = splitted[1]
        count = int(splitted[5])
        if name in names: # wenn es den Namen aus dem aktuell bearbeiteten Datensatz schon gibt
            names[name] =  names[name] + count # dann hole den zugehörigen Anzahlwert aus dem Dict und addiere den
            # aktuellen Wert
        else:
            names[name] = count # wenn der Namenseintrag im Dict noch nicht existiert, wird er eingetragen und als
            # zugehöriger Wert die Häufigkeit eingetragen. Somit wird das Dict nach und nach mit allen Namen der
            # csv-Datei befüllt und die Häufigkeit entsprechend aufaddiert

    max_occurences = 0
    name= ""
    for key,value in names.items():
        if max_occurences<value:
            max_occurences = value
            name = key


