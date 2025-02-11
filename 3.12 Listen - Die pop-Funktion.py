# So wie man mit Append einen Eintrag hinzufügen kann, kann man auch den letzten Eintrag einer Liste entfernen, hierzu gibt es die Pop-Funktion.

# Wir legen dazu erstmal eine Liste an.

planets = ["Merkus", "Venus", "Erde", "Mars", "Jupiter", "Saturn", "Uranus", "Neptun", "Pluto"]  # Liste wird angelegt
print(planets)  # Liste wird ausgegeben

planets.pop()  # Dieser Befehl entfernt den letzten Eintrag der Liste
print(planets)  # Liste wird ausgegeben - der letzte Eintrag fehlt

# Der Befehl pop löscht aber nicht nur den letzten Eintrag,sondern hat eigentlich auch einen Rückgabewert. Meist wird er aber ignoriert. Man könnte ihn aber auch anzeigen lassen
# oder gar weiterverarbeiten. Indem wir den Befehl in eine Print-Anweisung setzen (oder in eine Variable packen), könnten wir so beispielsweise ausgeben, welchen Wert der Befehl
# denn löscht. Man sollte aber beachten,dass auch beim Ausgeben dieses Rückgabewertes dieser Befehl ausgeführt wird. Indem ich den Rückgabewert mehrfach ausgebe, kann ich sehen,
# dass nach und nach die Einträge der Liste gelöscht werden


print(planets.pop())  # zeigt an, dass nun Neptun gelöscht wird
print(planets.pop())  # und nun Uranus
print(planets.pop())  # und nun Saturn
print(planets)  # Ausgabe: ['Merkus', 'Venus', 'Erde', 'Mars', 'Jupiter']
