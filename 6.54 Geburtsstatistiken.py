"""Wir wollen eine CSV-Datei öffnen und die ersten 5 Zeilen ausgeben"""
import matplotlib.pyplot as plt

"""with open("names.csv", "r") as file:  # Die Datei wird geöffnet
    counter = 0  # der Zähler wird auf 0 gesetzt
    for line in file:  # für jede Zeile der Datei tue folgendes:
        counter = counter + 1  # der Counter wird um 1 hochgesetzt
        print(line)  # die Zeile wird ausgegeben
        if counter >= 4:  # wenn der Zähler 4 oder größer ist, brich die Schleife ab
            break
"""
# Ausgabe:
# Id,Name,Year,Gender,State,Count
# 1,Mary,1910,F,AK,14
# 2,Annie,1910,F,AK,12
# 3,Anna,1910,F,AK,10
# im Grunde beinhaltet jeder Datensatz eine fortlaufende Nummer, einen Namen, ein Jahr, das Geschlecht, den Staat und die Häufigkeit des
# Namens. Diese Liste wollen wir nun in einem Diagramm ausgeben. Dazu erstellen wir nun erstmal wieder 2 Listen für die beiden Einheiten
# der Schenkel des Diagramms

"""xs = []
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
"""

# Nun wollen wir alle Zeilen finden, wo der Name "Anna" lautet, das Geschlecht Female und der Staat "CA" ist
"""name = "Anna"
gender = "F"
state = "CA"
with open("names.csv", "r") as file:  # Die Datei wird geöffnet
    counter = 0  # der Zähler wird auf 0 gesetzt
    for line in file:  # für jede Zeile der Datei tue folgendes:
        counter = counter + 1  # der Counter wird um 1 hochgesetzt
        line_splitted = line.strip().split(",")  # die Zeile wird gesplittet, es werden aber alle Leerzeichen am Zeilenanfang/ende entfernt
        if line_splitted[1] == name and line_splitted[3] == gender and line_splitted[4] == state:
            print(line_splitted)
# Ausgabe:
# ['356049', 'Anna', '1910', 'F', 'CA', '51']
# ['356277', 'Anna', '1911', 'F', 'CA', '57']
# ['356529', 'Anna', '1912', 'F', 'CA', '76']
# ['356836', 'Anna', '1913', 'F', 'CA', '86']
# ....
"""
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
        line_splitted = line.strip().split(",")  # die Zeile wird gesplittet, es werden aber alle Leerzeichen am Zeilenanfang/ende
        # entfernt und das Ergebnis in eine Liste namens line_splittet gesteckt
        if line_splitted[1] == name and line_splitted[3] == gender and line_splitted[4] == state:
            print(line_splitted)
            # hier werden die Zeilen gesucht, wo bestimmte Stellen des gesplitteten Datensatzes den Vorgaben entsprechen
            xs.append(int(line_splitted[2]))  # die jeweiligen Daten werden in die Liste xs bzw ys eingetragen
            ys.append(int(line_splitted[5]))
print(xs)
print(ys)


# Ausgabe:
# ['1910', '1911', '1912', '1913', '1914', '1915', '1916', '1917', '1918', '1919', '1920', '1921', '1922', '1923', '1924', '1925', '1926', '1927', '1928', '1929', '1930', '1931', '1932', '1933', '1934', '1935', '1936', '1937', '1938', '1939', '1940', '1941', '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014']
# ['51', '57', '76', '86', '95', '125', '139', '141', '137', '134', '170', '169', '155', '170', '167', '186', '158', '172', '164', '161',
# '138', '115', '128', '129', '137', '114', '106', '135', '107', '128', '99', '144', '140', '157', '134', '163', '189', '209', '234', '237', '251', '284', '280', '341', '384', '408', '465', '514', '500', '594', '608', '535', '596', '558', '612', '564', '585', '579', '496', '535', '570', '540', '537', '470', '487', '478', '494', '497', '556', '525', '569', '654', '593', '596', '576', '603', '628', '643', '714', '755', '758', '684', '649', '619', '683', '668', '638', '631', '521', '551', '694', '699', '653', '576', '586', '527', '444', '491', '418', '397', '357', '355', '365', '375', '462']

plt.plot(xs,ys) # plotte die Werte aus den Listen xs und ys
plt.show() # und zeige das Diagramm an

# Wichtig: Unbedingt beim Übergeben der Zahlenwert in die xs bzw ys-Liste die Zahlenwerte als int casten, weil sie sonst wie ein String
# behandelt werden