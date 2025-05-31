# --- Modul- und Paketstrukturen in Python ---
# In Python kannst du Code mithilfe von Ordnern (Paketen) und Dateien (Modulen) strukturieren.
# Diese Datei demonstriert, wie du ein Modul innerhalb eines Ordners (Pakets) definierst
# und wie die spezielle Datei __init__.py dabei eine Rolle spielt, um die Strukturierung
# und den Import von Code zu steuern.

# Schritt-für-Schritt-Erklärung der Paket-Erstellung (kann als Kommentar bleiben, wenn der Code nicht ausgeführt wird)
# 1. Wir legen einen Ordner namens 'hallom' an.
# 2. Im Ordner 'hallom' erstellen wir eine leere Datei namens '__init__.py'.
#    Diese Datei signalisiert Python, dass 'hallom' ein Python-Paket ist und importiert werden kann.
# 3. Im Ordner 'hallom' erstellen wir eine weitere Python-Datei namens 'datei.py',
#    in der eine Funktion f() definiert wird.

# --- Import-Methoden und deren Auswirkungen ---

# Methode 1: Direkter Import einer Datei aus dem Paket
# from hallom import datei
# datei.f()
# Ausgabe: datei.py - Funktion f()
# Dies ist die gängigste und oft empfohlene Methode, da sie explizit macht,
# woher die importierte Funktion kommt.

# ---
# Methode 2: Importiere alles (*) aus dem Paket (Vorsicht: __all__ steuert dies)
# Normalerweise wird der Stern-Import (from hallom import *) von Python unterbunden,
# um unübersichtliche Namensräume zu vermeiden.
# Um ihn zu erlauben, muss in der __init__.py des 'hallom'-Pakets die Variable __all__
# definiert werden, die eine Liste der öffentlich verfügbaren Module enthält.
from hallom import *
datei.f()
# Beispiel in __init__.py: __all__ = ["datei"]
# Diese Methode ist nützlich, wenn du nur bestimmte Teile eines Pakets exponieren möchtest
# oder wenn ein Paket viele kleine, eng verwandte Module enthält.

# ---
# Methode 3: Importiere das gesamte Paket und greife auf die Module zu
# Dies ist eine weitere explizite Methode, bei der du das Paket selbst importierst
# und dann über den Paketnamen auf die enthaltenen Module zugreifst.
# Um dies zu ermöglichen, muss in der __init__.py des 'hallom'-Pakets
# eine entsprechende Importanweisung hinzugefügt werden.
import hallom
hallom.datei.f()
# Beispiel in __init__.py: from . import datei
# Diese Methode kann bei größeren Paketen sinnvoll sein, um den vollen Pfad sichtbar zu machen.
