# Dictionaries und Schleifen
# In dieser Lektion lernen wir,wie wir einen Dictionary-Eintrag für Eintrag durchgehen können und wie man dabei das
# Entpacken von Tupeln braucht

d = {"München": "MUC", "Budapest": "BUD", "Helsinki": "HEL"}  # wir haben ein Dictionary erzeugt,das die Städtecodes den
# Orten zuweist

for key in d:
    print(key)  # das würde erstmal nur den Schlüsselwert der einzelnen Einträge ausgeben
    value = d[key]
    print(value)
# Ausgabe:
# München
# MUC
# Budapest
# BUD
# Helsinki
# HEL

# Es gibt eine Möglichkeit, einfacher an die Inhalte zu gelangen:
print(d.items())  # die Items-Funktion gibt die einzelnen Inhalte des Dictionaries in Listenähnlicher Form aus:
# Ausgabe:
# dict_items([('München', 'MUC'), ('Budapest', 'BUD'), ('Helsinki', 'HEL')])
for key, value in d.items():
    print(key + ":" + value)
# Ausgabe:
# München:MUC
# Budapest:BUD
# Helsinki:HEL
# Das heißt also,dass diese For-Schleife gleich 2 Werte aus der Rückgabe von d.items() für jeden Inhalt dieser Liste
# erhält und in die Variablen # key und value packt, diese dann ausgibt. key und value sind keine fixen Schlüsselworte,
# sondern frei wählbare Variablen