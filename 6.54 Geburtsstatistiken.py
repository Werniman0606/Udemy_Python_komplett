"""Wir wollen eine CSV-Datei öffnen und die ersten 5 Zeilen ausgeben"""

with open("names.csv", "r") as file:  # Die Datei wird geöffnet
    counter = 0  # der Zähler wird auf 0 gesetzt
    for line in file:  # für jede Zeile der Datei tue folgendes:
        counter = counter + 1  # der Counter wird um 1 hochgesetzt
        print(line)  # die Zeile wird ausgegeben
        if counter >= 4:  # wenn der Zähler 4 oder größer ist, brich die Schleife ab
            break
# Ausgabe:
# Id,Name,Year,Gender,State,Count
# 1,Mary,1910,F,AK,14
# 2,Annie,1910,F,AK,12
# 3,Anna,1910,F,AK,10
# im Grunde beinhaltet jeder Datensatz eine fortlaufende Nummer, einen Namen, ein Jahr, das Geschlecht, den Staat und die Häufigkeit des
# Namens. Diese Liste wollen wir nun in einem Diagramm ausgeben. Dazu erstellen wir nun erstmal wieder 2 Listen für die beiden Einheiten
# der Schenkel des Diagramms

xs = []
ys = []
with open("names.csv", "r") as file:  # Die Datei wird geöffnet
    counter = 0  # der Zähler wird auf 0 gesetzt
    for line in file:  # für jede Zeile der Datei tue folgendes:
        counter = counter + 1  # der Counter wird um 1 hochgesetzt
        print(line.strip().split(","))  # die Zeile wird ausgegeben, es werden aber alle Leerzeichen am Zeilenanfang/ende entfernt und am
        # Komma getrennt
        if counter >= 4:  # wenn der Zähler 4 oder größer ist, brich die Schleife ab
            break
# Ausgabe:
# ['Id', 'Name', 'Year', 'Gender', 'State', 'Count']
# ['1', 'Mary', '1910', 'F', 'AK', '14']
# ['2', 'Annie', '1910', 'F', 'AK', '12']
# ['3', 'Anna', '1910', 'F', 'AK', '10']


# Nun wollen wir alle Zeilen finden, wo der Name "Anna" lautet, das Geschlecht Female und der Staat "CA" ist
name = "Anna"
gender = "F"
state = "CA"
with open("names.csv", "r") as file:  # Die Datei wird geöffnet
    counter = 0  # der Zähler wird auf 0 gesetzt
    for line in file:  # für jede Zeile der Datei tue folgendes:
        counter = counter + 1  # der Counter wird um 1 hochgesetzt
        line_splitted=line.strip().split(",")  # die Zeile wird gesplittet, es werden aber alle Leerzeichen am Zeilenanfang/ende entfernt
        if line_splitted[1] == name and line_splitted[3]==gender and line_splitted[4]==state:
            print(line_splitted)
# Ausgabe:
# ['356049', 'Anna', '1910', 'F', 'CA', '51']
# ['356277', 'Anna', '1911', 'F', 'CA', '57']
# ['356529', 'Anna', '1912', 'F', 'CA', '76']
# ['356836', 'Anna', '1913', 'F', 'CA', '86']
# ....

# Nun wollen wir ein Diagramm zeichnen, welches auf der X-Achse die Jahre anzeigt und auf der Y-Achse, wie oft der Name vergeben wurde
xs = []
ys = []
name = "Anna"
gender = "F"
state = "CA"
with open("names.csv", "r") as file:  # Die Datei wird geöffnet
    counter = 0  # der Zähler wird auf 0 gesetzt
    for line in file:  # für jede Zeile der Datei tue folgendes:
        counter = counter + 1  # der Counter wird um 1 hochgesetzt
        line_splitted=line.strip().split(",")  # die Zeile wird gesplittet, es werden aber alle Leerzeichen am Zeilenanfang/ende entfernt
        if line_splitted[1] == name and line_splitted[3]==gender and line_splitted[4]==state: #hier werden die Zeilen gesucht,
            # wo bestimmte Stellen des gesplitteten Datensatzes den Vorgaben entsprechen
            xs.append(line_splitted[2]) #die jeweiligen Daten werden in die Liste xs bzw ys eingetragen
            ys.append(line_splitted[5])


print(xs)
print(ys)
