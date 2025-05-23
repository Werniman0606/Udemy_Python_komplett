# In dieser Lektion lernen wir, wie wir die Objektorientierung in Python nutzen, eine Klasse erstellen und was
# Methoden sind. Bisher haben wir immer mit Listen gearbeitet

students = ["Max", "Monika"]
students.append("Erik")
print(students)


# Streng genommen haben wir damit schon mit Objektorientierung gearbeitet, denn die Liste ist ein Objekt, welches mit
# der Funktion 'append' bearbeitet wurde. 'append' ist eine spezielle Funktion, die zu Listen gehört.
#
# Wir erstellen  einfach mal eine neue Objektklasse: Eine Klasse ist wie ein Bauplan oder eine Schablone, mit der wir
# Objekte # erstellen können.

class Student():
    pass


# Im Moment ist unsere 'Student'-Klasse noch sehr einfach. Sie dient als Bauplan, um Objekte vom Typ 'Student' zu
# erstellen.

# Wir erzeugen eine Funktion, die den Namen eines Studenten empfängt und dann den vollen Namen dieses Objektes
# zusammenbaut und ausgibt

def get_name(student):
    print(student.firstname + " " + student.lastname)


# Diese Funktion nimmt ein 'Student'-Objekt entgegen und greift auf dessen 'firstname'- und 'lastname'-Attribute zu.
# Nun erzeugen wir unser erstes Objekt namens erik, es soll vom Typ Student() sein Ein konkretes Objekt, das auf Basis
# einer Klasse erstellt wurde, nennen wir eine Instanz der Klasse.

erik = Student()
erik.firstname = "Erik"
erik.lastname = "Mustermann"
print(erik.firstname)  # Ausgabe: Erik # Der Vorname wird ausgegeben

get_name(erik)  # Ausgabe Erik Mustermann  # Die Funktion wird ausgeführt, welche den vollen Namen baut und ausgibt

# Und gleich noch eins

monika = Student()
monika.firstname = "Monika"
monika.lastname = "Musterfrau"
print(monika.lastname)  # Ausgabe: Musterfrau

get_name(monika)  # Ausgabe: Monika Musterfrau # Die Funktion wird ausgeführt, welche den vollen Namen baut und ausgibt


# Noch ein anderes Beispiel
# Wir erzeugen erstmal wieder eine Klasse. Auch hier dient die 'company'-Klasse als Bauplan für Firmen-Objekte,
# die spezifische Eigenschaften wie 'legal_name' und 'legal_type' haben können.

class company():
    pass


# Nun eine Funktion, die später für dieses Objekt ausgeführt wird

def get_name(company):
    print(company.legal_name + " " + company.legal_type)

c = company()  # eine neue Instanz des Objektes Company wird erstellt und die Instanz heißt c
c.legal_name = "Max Müller"  # Das Objekt bekommt einen Namen
c.legal_type = "GmbH"  # und einen Firmentyp
get_name(c)  # Ausgabe: Max Müller GmbH # Die Funktion wird ausgeführt, die aus Namen und Typ den vollständigen
# Namen generiert und ausgibt.

# Was passiert hier?
# In Zeile 56 wird ein Objekttyp generiert. Er hat keine standardmäßigen Inhalte, daher steht als Inhalt nur 'pass'
# drin.
# In Zeile 62 wird eine Funktion erzeugt, die einen Parameter empfängt, der in der internen Variable "company"
# gespeichert wird. Diese Funktion bastelt aus dem offiziellen Firmennamen der Objektinstanz und dem Firmentypen eine
# Ausgabe zusammen.
# In Zeile 65 wird überhaupt erst die Objektinstanz erzeugt und sie bekommt den Namen c.
# In Zeile 66+67 bekommt diese Instanz die Variablen für den Firmennamen und den Firmentyp zugewiesen
# In Zeile 68 wird die Funktion aufgerufen und ihr der Name der Instanz mitgenommen. Der Funktionsaufruf übergibt das
# c an die Funktion, die es als Variable company weiternutzt und dann aus dem für diese Instanz hinterlegten
# Variablen legal_name und legal_type den vollständigen Namen zusammenbastelt und ausgibt.

# Warum diese Reihenfolge? Weil die Definition einer Funktion immer VOR der ersten Nutzung erfolgen muss. In einer
# späteren Lektion werden wir sehen, dass es eine spezielle Methode namens 'init' gibt, mit der wir die Attribute
# eines Objekts direkt bei der Erstellung initialisieren können.

# Ein Hinweis noch: in unseren beiden Beispielen haben wir den gleichen Funktionsnamen benutzt. Das ist
# nicht ratsam. Daher ist es sinnvoll, statt einen allgemeinen Namen wie "get_names" zu nutzen,lieber etwas
# spezifisches wie "student_get_names" zu nutzen. Hintergrund: eine Funktion darf nicht unter dem gleichen Namen 2x
# vorhanden sein,weil sonst die 2.Funktion die erste überschriebt.

# In der Objektorientierten Programmierung könnten wir dieses krampfhafte Umbenennen der Funktionen in eindeutige
# Benennungen auch vereinfachen,indem wir die die Funktion/Methode einfach direkt in die Klassendefinition mit
# reinschreiben. Also so:
class Student():
    def name(self):
        print(self.firstname+ " " + self.lastname)
erik = Student()
erik.firstname = "Erik"
erik.lastname = "Mustermann"
erik.name()
# Was bedeutet dieses self ? Nun, das bedeutet,dass sich der Methodenaufruf automatisch immer auf das Objekt bezieht,
# für das die Methode aufgerufen wurde.D.h. der Aufruf von erik.name() bezieht sich immer auf das Objekt erik,
# für das die Methode aufgerufen wurde. Wir brauchen dem Methodenaufruf auch keinen Parameter mehr mitgeben

# Nun machen wir das auch für die Klasse Company

class company():
    def get_name(self):
        print(self.legal_name + " " + self.legal_type)

c = company()  # eine neue Instanz des Objektes Company wird erstellt und die Instanz heißt c
c.legal_name = "Max Müller"  # Das Objekt bekommt einen Namen
c.legal_type = "GmbH"  # und einen Firmentyp
c.get_name()  # Ausgabe: Max Müller GmbH #

# Woher weiß Python, welche der beiden Get-Name-Funktionen es ausführen muss ? Ganz einfach: vom dem vorangestellten
# Instanznamen weiß Python,um welche Klasse es sich handelt und ruft dann entsprechend die Methode auf,die in der
# Klassendefinition drinsteht
