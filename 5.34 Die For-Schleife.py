for i in range(0, 10):  # für die Reihe von 0 bis 10
    print(i)  # gib die aktuelle Zahl aus
# Ausgabe: 0...9

"""Der Befehl Range verhält sich ähnlich wie eine Liste,d.h. man kann mit einer Indexangabe auf ein bestimmtes Element zugreifen. Der Index beginnt dabei wieder mit 0 zu zählen"""
print(range(20, 30)[5])
# Ausgabe: 25
# Es wird die 20 ausgegeben, weil der Index 5 das 6.Element in der Reihe ist und das ist in diesem Fall die 25.

liste = [5, 8, 10]  # Eine Liste wird angelegt
for i in liste:  # Die einzelnen Elemente aus der Liste werden geholt..
    print(i)  # und ausgegeben.
