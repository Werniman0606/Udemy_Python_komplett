"""In dieser Lektion lernen wir,wie wir Daten umwandeln"""

a = "5"
b = "6"
print(a + b)  # Ausgabe: 56

# Warum kommt hier 56 raus statt -was zu erwarten wäre- 11 ? Das liegt daran, dass in den Variablen keine Zahlen,sondern Strings
# drinliegen. Diese werden durch den Plus-Operator einfach nur aneinandergehängt. Stattdessen müssen wir die Strings in eine ganze Zahl
# umwandeln

print(int(a) + int(b))  # Ausgabe: 11
# ------------------------------------------------------------------------------------------

# int sind aber immer ganze Zahlen. Aber was machen wir,wenn wir einen Kommawert haben ?

a = "5.2"
b = "4.7"

# print (int(a)+int(b)) würde hier einen Fehler ausgeben,weil man kommawerte nicht einfach in eine ganze Zahl umwandeln kann.  Statt int
# nehmen wir nun float, um eine Kommazahl zu erhalten

print(float(a) + float(b))  # Ausgabe: 9.9

# Das ganze muss man auch tun,wenn man einen Zahlenwert in einem String auszugeben

a = 49
# print("Ich bin " + a + " Jahre alt")  Das würde fehlschlagen,weil man Strings und Zahlen nicht mischen darf. Stattdessen casten wir die
# Zahl in einen String:

print("Ich bin " + str(a) + " Jahre alt") 
