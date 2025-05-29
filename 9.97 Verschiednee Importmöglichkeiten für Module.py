# In dieser Lektion wird gezeigt, dass Module bereits in vielen Anwendungen genutzt werden.

# Die folgende Zeile ist ein "Magic Command" für IPython/Jupyter Notebooks.
# Es stellt sicher, dass die erzeugten Matplotlib-Diagramme direkt im Notebook angezeigt werden.

# Importiert das 'pyplot'-Modul aus der Matplotlib-Bibliothek.
# 'pyplot' bietet eine einfache Schnittstelle zum Erstellen von Plots, ähnlich wie MATLAB.
import matplotlib.pyplot as plt

# Erstellt einen einfachen Liniengrafen.
# Der erste Array ([1, 2, 3]) definiert die x-Koordinaten der Punkte.
# Der zweite Array ([5, 4, 5]) definiert die entsprechenden y-Koordinaten der Punkte.
plt.plot([1,2,3],[5,4,5])

# Zeigt den erstellten Plot an.
plt.show()

# Ausgabe: Ein Diagramm, das drei Punkte (1,5), (2,4) und (3,5) miteinander verbindet,
# wodurch ein nach oben geöffnetes Dreieck entsteht.

#---

## Alternative Importmethoden für Module

# Man könnte die Abkürzung 'plt' auch weglassen.
# Dann müsste man aber immer den kompletten Modulnamen und das Untermodul angeben.
import matplotlib.pyplot
matplotlib.pyplot.plot([1,2,3],[5,4,5])
matplotlib.pyplot.show()

# Diese Methode ist weniger gebräuchlich, da sie den Code länger und unübersichtlicher macht.

#---

# Die dritte Art, eine Funktionalität zu importieren, wäre, nur einen Teil des Moduls zu importieren.
# Hier wird explizit nur das 'pyplot'-Untermodul aus 'matplotlib' importiert.
from matplotlib import pyplot
pyplot.plot([1,2,3],[5,4,5])
pyplot.show()

# Diese Methode ist nützlich, wenn man nur spezifische Untermodule oder Funktionen benötigt
# und den vollen Namen beibehalten möchte, aber den übergeordneten Modulnamen (hier 'matplotlib') nicht jedes Mal schreiben will.