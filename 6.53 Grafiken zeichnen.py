""" In dieser Lektion lernen wir, wie wir eine Grafikzeichnen können. Diese Kenntnisse werden in den folgenden Lektionen gebraucht"""

# Wir müssen dazu ein Modul zum Zeichnen einbinden

import matplotlib.pyplot as plt  # importiere die Funktion pyplot aus dem Modul matplotlib und benenne sie als plt

xs = [1, 2, 3]  # hier werden die Werte für die X-Achse als Liste angelegt
ys = [4, 7, 4]  # hier werden die Werte für die y-Achse als Liste angelegt
plt.plot(xs, ys)  # die Funktion plplot wird aufgerufen und es wird ihr gesagt, sie soll die Werte aus den Listen nehmen. Dabei werden die
# Werte immer relational zu ihrer Position in der Liste benutzt. D.h. der 1.Wert in der ersten Liste wird auch zusammen mit dem 1.Wert in
# der 2.Liste benutzt.
plt.show()  # nun wird das bisher im internen Speicher erzeugte Modul ausgegeben
