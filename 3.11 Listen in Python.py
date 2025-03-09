"""Hier ist ein Beispiel für eine Liste in Python:"""

meine_liste = [1, 2, 3, "Hallo", "Welt", 3.14]

"""
Erläuterung:

    meine_liste =: Dies erstellt eine Variable namens meine_liste und weist ihr eine Liste zu.
    []: Die eckigen Klammern kennzeichnen den Beginn und das Ende der Liste.
    1, 2, 3, "Hallo", "Welt", 3.14: Dies sind die Elemente der Liste. Eine Liste kann Elemente unterschiedlichen Datentyps enthalten (Zahlen, Zeichenketten, Fließkommazahlen usw.). Die Elemente werden durch Kommas getrennt.

Weitere Beispiele:"""

leere_liste = []  # Leere Liste
zahlen = [10, 20, 30, 40, 50]  # Liste mit Zahlen
namen = ["Alice", "Bob", "Charlie"]  # Liste mit Zeichenketten
wahr_falsch = [True, False, True]  # Liste mit booleschen Werten

"""Wichtige Eigenschaften von Listen:

    Geordnet: Die Elemente in einer Liste haben eine bestimmte Reihenfolge.
    Veränderbar (mutable): Du kannst Elemente in einer Liste hinzufügen, entfernen oder ändern.
    Indizierbar: Auf Elemente in einer Liste kannst du über ihren Index zugreifen (beginnend bei 0).

Beispiel für den Zugriff auf ein Element:"""

print(meine_liste[0])  # Gibt 1 aus (das erste Element)
print(meine_liste[3])  # Gibt "Hallo" aus (das vierte Element)

zahlen.append(99)
print(zahlen)

for i in zahlen:
    print(i)