"""Aufgabe
Finde heraus, wie oft der Name Max zwischen 1950 und 2000 in Kalifornien vergeben wurde.

"""

import matplotlib.pyplot as plt

xs = []
ys = []
name = "Max"
gender = "M"
state = "CA"
von = 1950
bis = 2000
with (open("names.csv", "r") as file):  # Die Datei wird geöffnet
    counter = 0  # der Zähler wird auf 0 gesetzt
    for line in file:  # für jede Zeile der Datei tue folgendes:
        line_splitted = line.strip().split(",")  # die Zeile wird gesplittet, es werden aber alle Leerzeichen am Zeilenanfang/ende
        # entfernt und das Ergebnis in eine Liste namens line_splittet gesteckt
        if line_splitted[1] == name and line_splitted[3] == gender and line_splitted[4] == state and int(line_splitted[2]) >= von and int(line_splitted[2]) <= bis:
        # wenn der Name stimmt,das Geschlecht stimmt, der Zeitraum und auch der Staat, dann
            counter = counter + int(line_splitted[5])  # wird der Counter wird um den aktuellen Anzahl-Wert hochgesetzt w
            print(line_splitted) # hier werden nochmal die einzelnen Zeilen ausgegeben, für die die If-Abfrage zutraf
print(f"Den Namen {name} gab es in diesem Zeitraum insgesamt {counter} mal.") # Und hier wird das Ergebnis ausgegeben
