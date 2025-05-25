"""
Vererbung ist ein fundamentales Konzept der Objektorientierung, mit der man Code besser strukturieren,
wiederverwenden und einfacher modellieren kann. In dieser Lektion lernen wir, was Vererbung ist und wie man sie in Python benutzt.
"""

# ---
## Teil 1: Start ohne Vererbung - Redundanz erkennen

# Wir erstellen zuerst eine grundlegende Klasse für einen 'Student'.
class Student():
    # Der Konstruktor '__init__' wird aufgerufen, wenn ein neues Student-Objekt erstellt wird.
    # Er nimmt 'firstname' (Vorname) und 'surname' (Nachname) entgegen und speichert sie als Eigenschaften des Objekts.
    def __init__(self, firstname, surname):
        self.firstname = firstname   # Speichert den Vornamen.
        self.surname = surname     # Speichert den Nachnamen.

    # Diese Methode gibt den vollständigen Namen des Studenten zurück.
    def name(self):
        return self.firstname + " " + self.surname

# Wir erstellen ein Student-Objekt.
student = Student("Max", "Müller")
# Wir rufen die 'name()'-Methode auf und geben das Ergebnis aus.
print(student.name())
# Ausgabe: Max Müller

# ---
# Nun gibt es aber eine weitere Art von Studenten: solche, die bereits im Berufsleben stehen.
# Die Besonderheit bei ihnen ist, dass sie noch einen Arbeitgebernamen haben.

# Hier erstellen wir eine separate 'Student'-Klasse (eine Wiederholung der oberen, aber für den Vergleich nützlich).
class Student():
    def __init__(self, firstname, surname):
        self.firstname = firstname
        self.surname = surname

    def name(self):
        return self.firstname + " " + self.surname

# Dies ist eine neue Klasse für einen 'WorkingStudent' (Berufstätiger Student).
# Beachte, dass sie am Anfang sehr ähnlich zur 'Student'-Klasse ist.
class WorkingStudent():
    # Der Konstruktor für den WorkingStudent. Er braucht zusätzlich den 'company'-Namen.
    def __init__(self, firstname, surname, company):
        self.firstname = firstname   # Speichert den Vornamen.
        self.surname = surname     # Speichert den Nachnamen.
        self.company = company     # Speichert den Firmennamen, der für WorkingStudent neu ist.

    # Diese Methode gibt den vollständigen Namen und den Firmennamen zurück.
    # Beachte, dass sie fast identisch zur 'name()'-Methode von 'Student' ist, aber erweitert wurde.
    def name(self):
        return self.firstname + " " + self.surname + ", " + self.company

# Wir erstellen ein WorkingStudent-Objekt.
student2 = WorkingStudent("Heinz", "Schulze", "ABCDEF Gmbh")
# Wir rufen die 'name()'-Methode auf und geben das Ergebnis aus.
print(student2.name())
# Ausgabe: Heinz Schulze, ABCDEF Gmbh

# Wie wir sehen, haben wir im Grunde zwei vollkommen voneinander unabhängige Klassen geschrieben,
# die viel doppelten Code enthalten (z.B. 'firstname', 'surname', und der Anfang der 'name()'-Methode).
# Das bläht den Code unnötig auf und macht ihn schwerer zu pflegen.
# Sinnvoll wäre es doch, wenn die Klasse 'WorkingStudent' alle gemeinsamen Eigenschaften von 'Student' erben könnte,
# sodass man nicht alles doppelt anlegen muss. Genau dafür gibt es die **Vererbung**.

# ---
## Teil 2: Vererbung nutzen - Code wiederverwenden

# Wir können die Eigenschaften von 'Student' ganz einfach an 'WorkingStudent' vererben.
# Dazu geben wir der Klassendefinition von 'WorkingStudent' einfach in ihren Klammern die Klasse 'Student' mit,
# von der sie erben soll. Das macht 'Student' zur **Elternklasse** (oder Basisklasse) und 'WorkingStudent' zur **Kindklasse** (oder abgeleiteten Klasse).

class Student():
    def __init__(self, firstname, surname):
        self.firstname = firstname
        self.surname = surname

    def name(self):
        return self.firstname + " " + self.surname

# 'WorkingStudent' erbt jetzt von 'Student'. Das bedeutet, es bekommt automatisch alle
# Methoden und Eigenschaften von 'Student' "geschenkt".
class WorkingStudent(Student): # <- Hier geben wir 'Student' in den Klammern an.
    def __init__(self, firstname, surname, company):
        # 'super().__init__(firstname, surname)' ruft den Konstruktor der Elternklasse (Student) auf.
        # Dies ist sehr wichtig! Es stellt sicher, dass die 'firstname' und 'surname'
        # Eigenschaften von der Elternklasse initialisiert werden, ohne dass wir es hier doppelt schreiben müssen.
        # Es ist, als würden wir sagen: "Liebe Elternklasse, mach du zuerst deinen Teil der Initialisierung!"
        # Man übergibt hier die Argumente, die der Konstruktor der Elternklasse erwartet.
        super().__init__(firstname, surname)
        # Jetzt initialisieren wir die zusätzlichen Eigenschaften, die nur für 'WorkingStudent' gelten.
        self.company = company

    # Wir überschreiben (overriding) die 'name()'-Methode der Elternklasse.
    # Das bedeutet, wenn man 'name()' auf einem 'WorkingStudent'-Objekt aufruft,
    # wird diese spezielle Version ausgeführt und nicht die der Elternklasse.
    def name(self):
        return self.firstname + " " + self.surname + ", " + self.company
        # Alternative Schreibweise für 'name()', die zeigt, wie man die Elternmethode aufrufen kann:
        # def name(self):
        #    # 'super().name()' ruft die 'name()'-Methode der Elternklasse auf ('Student.name()').
        #    # Das Ergebnis (z.B. "Heinz Schulze") wird dann hier weiterverwendet.
        #    return super().name() + ", " + self.company
        # Diese Variante ist oft sauberer, da man sich nicht darum kümmern muss, wie die Elternklasse den Namen genau zusammensetzt.

# Wir erstellen ein WorkingStudent-Objekt.
student2 = WorkingStudent("Heinz", "Schulze", "ABCDEF Gmbh")
# Da 'WorkingStudent' von 'Student' erbt und die 'name()'-Methode überschreibt,
# wird die spezielle 'name()'-Methode von 'WorkingStudent' ausgeführt.
print(student2.name())
# Ausgabe: Heinz Schulze, ABCDEF Gmbh

# ---
## Teil 3: Polymorphie - Flexibilität durch Vererbung

# Noch ein Beispiel: Wir haben eine Liste mit verschiedenen Objekten, die von 'Student' abstammen (entweder 'Student' selbst oder 'WorkingStudent').
students = [
    WorkingStudent("Max", "Müller", "Pleite KG"), # Ein WorkingStudent
    Student("Monika", "Mustermann"),              # Ein normaler Student
    Student("Erik", "Essklein"),                  # Ein normaler Student
    WorkingStudent("Franziska", "Mustermann", "Insolvenzia Gmbh") # Ein WorkingStudent
]

print("\n--- Alle Studenten und Werkstudenten ausgeben ---")
# Wir gehen die Liste 'students' Element für Element durch.
for student_item in students: # Der Name 'student_item' ist hier gewählt, um Verwirrung mit der Klasse 'Student' zu vermeiden.
    # Für jedes Objekt in der Liste rufen wir die 'name()'-Methode auf.
    # Was passiert hier? Python ist "schlau" genug, um zu erkennen, welchen Typ das aktuelle 'student_item' hat.
    # - Wenn es ein 'Student'-Objekt ist, wird die 'name()'-Methode aus der 'Student'-Klasse ausgeführt.
    # - Wenn es ein 'WorkingStudent'-Objekt ist, wird die **überschriebene** 'name()'-Methode aus der 'WorkingStudent'-Klasse ausgeführt.
    # Dieses Verhalten, dass dieselbe Methode auf verschiedenen Objekttypen unterschiedliche Dinge tut,
    # nennt man **Polymorphie** (Vielgestaltigkeit). Es ist ein sehr mächtiges Konzept der Vererbung.
    print(student_item.name())

# Erwartete Ausgabe:
# Max Müller, Pleite KG
# Monika Mustermann
# Erik Essklein
# Franziska Mustermann, Insolvenzia Gmbh