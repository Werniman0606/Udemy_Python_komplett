# Typen feststellen
# Manchmal möchte man in Python feststellen,ob eine Variable einen bestimmten Typen hat oder nicht. Dafür kann man
# "isinstance" bzw "type" verwenden. In dieser Lektion lernen wir, wie man isinstance verwendet oder den type
# feststellt und was der Unterschied ist

class Student():
    # Der **Konstruktor** (__init__):
    # Diese Methode wird automatisch aufgerufen, wenn du ein neues Student-Objekt erstellst.
    # Sie initialisiert die grundlegenden Eigenschaften eines Studenten.
    def __init__(self,firstname,surname):
        # 'self.firstname' und 'self.surname' sind **Instanzvariablen**.
        # Sie speichern den Vornamen und Nachnamen für JEDES spezifische Student-Objekt,
        # das von dieser Klasse erstellt wird.
        self.firstname = firstname
        self.surname = surname

    ## Die 'name'-Methode: Eine Methode, die den vollständigen Namen des Studenten zurückgibt.
    def name(self):
        return self.firstname + " " + self.surname

# --- Unterklasse: WorkingStudent ---
# Diese Klasse repräsentiert einen Studenten, der zusätzlich arbeitet.
# Sie **erbt** von der Klasse 'Student', was durch '(Student)' nach dem Klassennamen angezeigt wird.
# Das bedeutet, ein WorkingStudent ist auch ein Student und erbt dessen Eigenschaften und Methoden.
class WorkingStudent(Student):
    # Der **Konstruktor** der Unterklasse:
    # Auch diese Methode wird beim Erstellen eines WorkingStudent-Objekts aufgerufen.
    # Sie muss die Initialisierung sowohl der Elternklasse als auch der eigenen,
    # spezifischen Eigenschaften übernehmen.
    def __init__(self,firstname,surname,company):
        # **super().__init__(firstname, surname)**:
        # Dies ist der entscheidende Teil der Vererbung! Es ruft den Konstruktor
        # der **Elternklasse** (Student) auf.
        # Dadurch werden 'self.firstname' und 'self.surname' wie gewohnt initialisiert,
        # ohne dass wir den Code dafür in WorkingStudent wiederholen müssen.
        super().__init__(firstname,surname)
        # Eigene Eigenschaft des WorkingStudent:
        # Zusätzlich zu den Eigenschaften, die von 'Student' geerbt wurden,
        # hat ein WorkingStudent noch eine 'company'.
        self.company = company

#2 Objekte werden angelegt, von jeder Klasse eins
w_student = WorkingStudent("Max","Müller","Pleite KG")
student = Student("Monika","Mustermann")

print(type(w_student))
# Ausgabe:<class '__main__.WorkingStudent'>,d.h. es handelt sich um ein Objekt vom Type WorkingStudent
print(type(student))
# Ausgabe: <class '__main__.Student'>, d.h. es handelt sich um einen normalen Studenten

if type(student) == Student: # es wird geprüft,ob das Objekt student vom Typ Student ist
    print("Diese Zeile wird für einen Studenten ausgegeben")

print(isinstance(w_student,WorkingStudent)) # es wird geprüft,ob das Objekt w_student vom Typ Workingstudent ist
#Ausgabe: True # Da das zutrifft, wird "True" ausgegeben

print(isinstance(w_student,Student)) # es wird geprüft,ob das Objekt w_student vom Typ Student ist
#Ausgabe: True # Da das zutrifft, wird "True" ausgegeben

# Warum bekommen wir hier in beiden Fällen ein True,obwohl der w_student eigentlich ein WorkingStudent ist ? Das
# liegt daran,dass WorkingStudent ja durch die Vererbung eine Erweiterung von Student ist

# Der Unterschied zwischen Type und isinstance ist also, dass bei isinstance auch betrachtet wird,ob ein Objekt
# vielleicht ein "Kind" einer anderen Klasse ist, bei Type ist das nicht der Fall.

# Wo wird sowas angewendet ? Beispielsweise wenn man wieder eine Liste mit mehreren Objekten hat, deren Typ man
# feststellen will.

students = [
    WorkingStudent("Max", "Müller", "Pleite KG"), # Ein WorkingStudent
    Student("Monika", "Mustermann"),              # Ein normaler Student
    Student("Erik", "Essklein"),                  # Ein normaler Student
    WorkingStudent("Franziska", "Mustermann", "Insolvenzia Gmbh") # Ein WorkingStudent
]

for student in students: # für jeden Eintrag in der Liste
    if isinstance(student,WorkingStudent): # wird gecheckt,ob der aktuell geprüfte Eintrag vom Typ WorkingStudent ist
        print(student.name()) # und ggf. der Name des Studenten ausgegeben
        # Ausgabe:
        # Max Müller
        # Franziska Mustermann
