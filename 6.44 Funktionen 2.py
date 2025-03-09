""" In der vorherigen Lektion haben wir gelernt, wie wir eine Funktion anlegen, die ohne Parameter gestartet werden können. Nun machen wir das gleiche mit Funktionen mit
Parametern"""


def multi_print(name, count):  # Die Parameter werden empfangen und in 2 interne Variablen gespeichert
    for i in range(0, count):  # eine Schleife wird erzeugt, die so oft läuft,wie die Variable count besagt
        print(name)  # der Text wird ausgegeben


multi_print("Marco", 10)  # Die Funktion wird aufgerufen und es werden eine Stringvariable und ein Int-Wert übergeben
# Ausgabe
# Marco
# Marco
# ...
# Marco
# (insgesamt 10x)


# Wir können Funktionen aber auch ineinander verschacheln:
def weitere_funktion():  # eine neue Funktion wird angelegt
    multi_print("Marco", 10)  # beim Ausführen wird die Funktion multi_print ausgeführt und 2 Parameter mitgegeben
    multi_print("Sandra", 10)  # und nochmal wird multi_print ausgeführt und 2 Parameter mitgegeben

weitere_funktion() # die Funktion wird ausgeführt
# Ausgabe:
# Marco (10x)
# Sandra (10x)


def maximum(a,b): #eine neue Funktion wird angelegt. Sie empfängt 2 Parameter
    if a<b: #wenn a kleiner als b ist,
        return b #wird b an die aufrufende Stelle zurückgegeben
    else: # ansonsten
        return a # wird a zurückgegeben

print(maximum(6,13))
# Ausgabe: 13
# Es wird 13 zurückgegeben, da der 1.Wert kleiner als der 2.Wert ist,d.h. b wird zurückgegeben. Und da der Aufruf innerhalb einer Printanweisung steht, wird der zurückgegebene
# Wert ausgegeben.



