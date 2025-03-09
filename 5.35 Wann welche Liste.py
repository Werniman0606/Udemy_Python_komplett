"""Nun haben wir sowohl die For- als auch die While-Schleife kennengelernt. Aber wann verwenden wir welche Schleife ?"""


# wir legen eine While-Schleife an. Sie läuft, bis die Bedingung erfüllt ist, was aber erfortdert, dass sich der zu prüfende Wert auch innerhalb der Schleife ändert
counter = 0
while counter < 10:
    print(counter)
    counter = counter + 1
# Ausgabe 0...9


# Die For-Schleife ist eher geeignet, wenn man vorab schon weiß, wie oft die Schleife laufen soll
for counter in range (0,10):
    print(counter)
# Ausgabe 0...9

