# In Python ist alles ein Objekt – sogar eine Zahl ist eine Instanz einer Klasse.
# Das schauen wir uns jetzt genauer an.

# Beispiel 1: Zahlen sind Objekte
a = 12.5
print(type(a))
# Ausgabe: <class 'float'>
print(a + 5)
# Ausgabe: 17.5
# Intern ruft Python für die Addition die spezielle Methode __add__ auf.
print(a.__add__(5))
# Ausgabe: 17.5
# Man sieht hier, dass 'a + 5' nur eine "syntaktische Zucker"-Schreibweise für 'a.__add__(5)' ist.

# Beispiel 2: Strings sind Objekte
s = "Hallo Welt"
print(type(s))
# Ausgabe: <class 'str'>

print(len(s))
# Ausgabe: 10
# Die eingebaute Funktion len() ruft im Hintergrund die __len__-Methode des String-Objekts auf.
print(s.__len__())
# Ausgabe: 10

# Beispiel 3: Listen sind auch Objekte
my_list = [1, 2, 3]
print(type(my_list))
# Ausgabe: <class 'list'>

# Listen haben ebenfalls Methoden, da sie Objekte sind.
my_list.append(4)
print(my_list)
# Ausgabe: [1, 2, 3, 4]

# Eine weitere Methode einer Liste
my_list.reverse()
print(my_list)
# Ausgabe: [4, 3, 2, 1]

# Beispiel 4: Boolesche Werte sind Objekte (Instanzen der Klasse 'bool')
is_true = True
print(type(is_true))
# Ausgabe: <class 'bool'>

# Auch 'None' ist ein Objekt
nothing = None
print(type(nothing))
# Ausgabe: <class 'NoneType'>