# Das ist die Schleife, wie wir sie bisher schreiben würde. Sie würde 10x durchlaufen.
for counter in range(0, 10):
    print(counter)
# Ausgabe 0...9

# Aber was machen wir,wenn diese Schleife schon abbrechen soll,wenn der Wert von counter 5 ist ? In dem Fall bauen wir eine If-Abfrage ein, die die Schleife abbricht
for counter in range(0, 10):
    if counter == 3:
        break
    print(counter)
# Ausgabe 0...2

#Wir können aber auch bewirken, dass die Schleife bei einem bestimmten Punkt erneut beginnt, um z.B. einen bestimmten Wert auszulassen
for counter in range(0, 10):
    if counter == 3: # wenn die Variable den Wert 3 hat
        continue #setze die Schleife fort,d.h. wenn sie 3 ist, wir der folgende print-Befehl gar nicht ausgeführt,sondern die Schleife an der nächsten Stelle weitergeführt
    print(counter)
# Ausgabe 0..1..2..4..5..6..7..8..9

