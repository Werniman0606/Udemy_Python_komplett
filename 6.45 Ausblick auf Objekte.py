#In Python arbeiten wir mit Objekten. So ist zum Beispiel eine Liste schonmal ein Objekt, die mit einer Funktion bearbeitet werden kann

liste = [1,2,3] #Liste wird angelegt
print(liste) # Liste wird ausgegeben
#Ausgabe: [1,2,3]

liste.append(4)
print(liste)
#Ausgabe: [1,2,3,4]

"""Das bedeutet, dass die Liste ein Objekt ist und das durch einen Punkt angehängte Append eine Funktion ist, die auf das Listenobjekt wirkt."""

# Man kann aber auch einfache Strings durch Funktionen trennen, d.h. selbst Strings sind schon objekte
print("Hallo,Welt".split(",")) # Das Objekt "Hallo,Welt" wird getrennt, als Trennzeichen wird das Komma angenommen. Zurückgegeben wird eine Liste