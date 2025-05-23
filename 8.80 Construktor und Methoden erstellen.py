# In dieser Lektion lernen wir, wie man mit Hilfe eines Construktors Eigenschaften einer Klasse definieren kann und
# wie man Eigenschaften einer Instanz ändert

# In der letzten Lektion haben wir folgendes kleines Programm geschrieben:
# class Student():
#    def name(self):
#        print(self.firstname+ " " + self.lastname)
# erik = Student()
# erik.firstname = "Erik"
# erik.lastname = "Mustermann"
# erik.name()

# Wenn wir aber vergessen, z.B. den Firstname zu definieren (Zeile 9),dann läuft die Methode nicht durch und es gibt
# einen Attribute Error, weil der Versuch,den firstname auszulesen, schiefgeht.
# Um dem vorzubeugen,wäre es sinnvoll,wenn wir schon beim Anlegen eines Eintrags sicherstellen können,dass firstname
# und lastname vorhanden sind. Statt der oben gezeigten Schreibweise möchten wir den Code also lieber so schreiben
# können und uns die getrennte Eintragung von first und lastname ersparen:
# class Student():
#    def name(self):
#        print(self.firstname+ " " + self.lastname)
# erik = Student("Erik","Mustermann")
# erik.name()

# Wir legen nun einfach einen neuen Eintrag in der Klassendefinition an:
class Student():
    def __init__(self, firstname, lastname):  # hier beginnt der Construktor. Er kommt automatisch zum Einsatz,
        # wenn ich eine neue Instanz des Objektes anlege
        self.firstname = firstname  # der empfangene Wert für firstname wird in die gleichnamige Variable übertragen
        self.lastname = lastname  # der empfange Wert für lastname wird in die gleichnamige Variable übertragen
        self.term = 1  # eine Default-Variable wird mit dem Wert 1 gefüllt

    def name(self):
        print(self.firstname + " " + self.lastname + " (Semester: " + str(self.term) + ")")  # die 3 im Construktor
        # angelegten Variablen werden ausgegeben


erik = Student("Erik", "Mustermann")  # hier wird eine neue Instanz der Klasse Student erzeugt. Sie erhält den Namen
# erik und ist von der Klasse Student
erik.term = erik.term + 1
erik.name()


# Das hochzählen in Zeile 39 ist jedoch fehlerträchtig, weil man sie so ziemlich leicht überschreiben kann. Daher
# verschieben wir dies in eine eigene Methode innerhalb des Construktors:
class Student():
    def __init__(self, firstname, lastname):  # hier beginnt der Construktor. Er kommt automatisch zum Einsatz,
        # wenn ich eine neue Instanz des Objektes anlege
        self.firstname = firstname  # der empfangene Wert für firstname wird in die gleichnamige Variable übertragen
        self.lastname = lastname  # der empfange Wert für lastname wird in die gleichnamige Variable übertragen
        self.term = 1  # eine Default-Variable wird mit dem Wert 1 gefüllt

    def increase_term(self): # Beim aufruf dieser Funktion wird die Variable Term um 1 hochgezählt
        self.term = self.term + 1

    def name(self):
        print(self.firstname + " " + self.lastname + " (Semester: " + str(self.term) + ")")  # die 3 im Construktor
        # angelegten Variablen werden ausgegeben


erik = Student("Erik", "Mustermann")  # hier wird eine neue Instanz der Klasse Student erzeugt. Sie erhält den Namen
# erik und ist von der Klasse Student
erik.increase_term()
erik.name() # Ausgabe: Erik Mustermann (Semester: 2)

