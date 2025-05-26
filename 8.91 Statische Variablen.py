# Verständnis von Klassen- und Instanzvariablen in Python

# Was man in vielen anderen Programmiersprachen als "statische Variable" bezeichnen würde,
# ist in Python in der Regel eine **Klassenvariable**.
# Eine Klassenvariable ist eine Variable, die **allen Instanzen** einer Klasse gemeinsam ist.
# Sie gehört zur Klasse selbst, nicht zu einer spezifischen Instanz.

# Beispiel 1: Klassenvariable

class Car:
    # 'price' ist hier eine Klassenvariable.
    # Alle Objekte der Klasse 'Car' teilen sich diese Variable und ihren Wert.
    price = "expensive"


# Ein Objekt (Instanz) der Klasse wird erzeugt
c = Car()
# Der Inhalt der Klassenvariable 'price' wird über die Instanz ausgegeben
print(c.price)
# Ausgabe: expensive

# Wichtig: Klassenvariablen können direkt über die Klasse geändert werden.
# Wenn man die Klassenvariable über die Klasse überschreibt,
# ändert sich der Wert für *alle* bestehenden und zukünftigen Instanzen,
# die keinen eigenen Wert für diese Variable definiert haben.
Car.price = "cheap"
print(Car.price)  # Zugriff über die Klasse
# Ausgabe: cheap
print(c.price)  # Zugriff über die Instanz (der Wert hat sich ebenfalls geändert)


# Ausgabe: cheap

# Wenn Sie ein Verhalten wünschen, bei dem jede Instanz ihren eigenen,
# unabhängigen Wert für eine Variable hat, benötigen Sie eine **Instanzvariable**.

# ---
# Beispiel 2: Instanzvariable

class NewCar:
    # Der Konstruktor '__init__' wird aufgerufen, wenn ein neues Objekt (Instanz) erstellt wird.
    def __init__(self):
        # 'self.price' ist eine Instanzvariable.
        # Jede Instanz von 'NewCar' erhält ihre *eigene Kopie* dieser Variable.
        self.price = "expensive"


# Erzeugen der ersten Instanz
car1 = NewCar()
print(car1.price)
# Ausgabe: expensive

# Erzeugen einer zweiten Instanz
car2 = NewCar()
print(car2.price)
# Ausgabe: expensive

# Wenn wir nun die 'price'-Variable einer bestimmten Instanz ändern,
# betrifft dies nur diese eine Instanz:
car1.price = "very expensive"

print(car1.price)
# Ausgabe: very expensive (nur car1 wurde geändert)
print(car2.price)
# Ausgabe: expensive (car2 behält seinen ursprünglichen Wert, da es eine eigene Instanzvariable ist)

# Fazit:
# - **Klassenvariablen** (wie 'price' in Beispiel 1) gehören zur Klasse und werden von allen Instanzen geteilt.
#   Änderungen über die Klasse wirken sich auf alle Instanzen aus (solange die Instanzen keine eigene Variable des gleichen Namens haben).
# - **Instanzvariablen** (wie 'self.price' in Beispiel 2) gehören zu einer spezifischen Instanz.
#   Jede Instanz hat ihre eigene Kopie, und Änderungen an einer Instanz wirken sich nicht auf andere Instanzen aus.
