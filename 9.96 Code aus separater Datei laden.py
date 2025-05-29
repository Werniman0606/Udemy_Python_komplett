# Module in Python

# Module ermöglichen es, Code in wiederverwendbare Einheiten zu strukturieren.
# In dieser Lektion erstellst du ein einfaches Modul und importierst es in ein Hauptprogramm.

# Zuerst erstellen wir eine Python-Datei namens 'hallo.py' mit zwei Funktionen,
# die unterschiedliche Begrüßungen ausgeben.

# Importieren des Moduls 'hallo'
import hallo

# Das `print()` der importierten Modulvariable zeigt den Pfad zur Moduldatei an.
print(hallo) # Beispiel-Ausgabe: <module 'hallo' from 'C:\\Users\\wilco\\PycharmProjects\\Udemy_Python_komplett_neu\\hallo.py'>

# Ausführen der Funktionen aus dem Modul.
# Die Funktionen müssen mit dem Modulnamen präfixiert werden (z.B. hallo.welt()).
hallo.welt() # Ausgabe: Hallo Welt
hallo.mars() # Ausgabe: Hallo Mars

---

# Eine alternative Methode zum Importieren spezifischer Funktionen

# Mit 'from <Modul> import <Funktion1>, <Funktion2>' importierst du nur ausgewählte Funktionen.
# Dies ermöglicht die direkte Verwendung der Funktion ohne den Modulnamen.
from hallo import welt, mars

# Die Funktionen können nun direkt aufgerufen werden, da sie spezifisch importiert wurden.
welt() # Ausgabe: Hallo Welt
mars() # Hallo Mars

# Der Hauptunterschied zwischen 'import hallo' und 'from hallo import ...' ist:
# - 'import hallo': Importiert das gesamte Modul, Funktionen müssen mit 'hallo.' aufgerufen werden.
# - 'from hallo import welt, mars': Importiert nur die genannten Funktionen, die dann direkt nutzbar sind.

---

# Importieren aller Funktionen aus einem Modul (Nicht empfohlener Stil)

# 'from hallo import *' importiert alle Funktionen und Klassen aus dem Modul.
# Dadurch entfällt die Notwendigkeit, den Modulnamen beim Aufruf anzugeben.
from hallo import *

welt() # Ausgabe: Hallo Welt
mars() # Ausgabe: Hallo Mars

# **Hinweis:** Das Importieren aller Elemente mit '*' wird im Allgemeinen als schlechter Programmierstil betrachtet,
# da es zu Namenskollisionen führen kann und die Herkunft von Funktionen unklar macht.