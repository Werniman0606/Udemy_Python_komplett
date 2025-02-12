# Wenn wir Werte vergleichen wollen, könnten wir das mit einer IF-Anweisung tun:
if (4 < 5):
    print("JA")  # Ausgabe: "JA", weil 4 nunmal kleiner als 5 ist

# Intern gesehen arbeiten sollte Vergleiche aber mit Boolschen Werten,d.h. der Rückgabewert solcher Vergleiche ist eigentlich TRUE oder
# FALSE

print(4 < 5)  # Ausgabe: True, weil ja 4 tatsächlich kleiner ist als 5.
print(5 < 4)  # Ausgabe: False, weil 5 nicht kleiner als 4 ist

# Man kann den Bool-Wert auch direkt in einer Variable speichern:
b = False   # Wichtig: Boolwerte beginnen IMMER mit einem Großbuchstaben


result = 5<6  # Die Abfrage wird gecheckt und der Rückgabewert True in eine Variable gepackt
if result: # man kann bei der Prüfung, ob ein Wert True ist, den Vergleichsoperator = weglassen, dann prüft Python automatisch,
    # ob die Boolvariable auf True ist. Den Vergleichsoperator = muss man nur nutzen,wenn man prüfen will, ob die Variable False ist.
    print("5 ist kleiner als 6") # Die Zeile wird ausgegeben,weil ja 5 tatsächlich kleiner als 6 ist, somit die If-Abfrage stimmt und
    # folglich die Printanweisung ausgeführt wird.

# Man kann aber auch Variablen darauf prüfen,ob sie identisch sind. Dazu nimmt man den ==-Operator, der ebenfalls einen Boolwert ausgibg
a = 5
b = 5
print(a==b) # Ausgabe: True, weil a ja tatsächlich identisch mit b ist.

# Es gibt aber auch einen Ungleichoperator, der != heißt
word = "Hallo"
print(word != "Hallo") #Ausgabe: False, denn die Variable ist ja NICHT ungleich "Hallo",
print(word != "Huhu") # Ausgabe: True, denn die Variable ist ja tatsächlich anders als "Huhu"

