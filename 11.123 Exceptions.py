""" Exceptions in Python

In dieser Lektion lernst du,
a) wie du damit umgehst, wenn während der Laufzeit deines Programmes ein Fehler auftritt

Manche Befehle führen zu einem Fehler, wenn du sie versuchst. Etwa wenn man versucht, durch 0 zu teilen, dann gibt
es einen ZeroDivisionError. Oder wenn man versucht, eine nicht existente Datei zu nutzen, gibts einen FilenotFoundError.

Das können wir umgehen, indem wir die Fehlermeldung abfangen. Das geht mit einer Try-Anweisung und einer
Except-Anweisung:
"""

# Der 'try'-Block:
# Code, der möglicherweise einen Fehler (eine Exception) auslösen könnte,
# wird hier platziert. Wenn im 'try'-Block ein Fehler auftritt,
# wird die Ausführung des 'try'-Blocks sofort gestoppt, und Python sucht
# nach einem passenden 'except'-Block, um den Fehler zu behandeln.
try:
    print(5/0) # Dieser Befehl wird einen ZeroDivisionError auslösen,
               # da eine Division durch Null nicht definiert ist.

# Der 'except'-Block:
# Dieser Block wird ausgeführt, wenn im zugehörigen 'try'-Block eine
# spezifische Exception auftritt, die hier genannt wird.
# In diesem Fall fangen wir einen 'ZeroDivisionError' ab.
except ZeroDivisionError:
    # Diese Nachricht wird ausgegeben, wenn ein ZeroDivisionError gefangen wurde.
    # Sie informiert den Benutzer über das Problem, ohne das Programm abstürzen zu lassen.
    print("Ey du Spacken, durch 0 teilen ist nicht erlaubt!")

# Dieser Befehl wird nach der Fehlermeldung ausgeführt.
# Er zeigt, dass das Programm nach dem Abfangen des Fehlers normal weiterläuft.
print(5)