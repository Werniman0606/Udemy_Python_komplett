# In dieser Lektion lernen wir, wie man einen Tupel verwenden kann,um mehrere Rückgabewerte einer Funktion zu
# modellieren und wie man Tupel wieder entpacken kann

student = ("Max Müller",22,"Informatik") # Wir haben ein Tupel mit 3 unterschiedliche Rückgabewerte zu verpacken

# Um die Werte auszulesen, könnte man theoretisch die einzelnen Werte in Variablen kopieren, was aber wahnsinnig
# aufwändig ist
name = student[0]
age = student[1]
subject = student[2]
print(name)
print(age)
print(subject)
# Ausgabe:
# Max Müller
# 22
# Informatik

# Einfacher wäre es, wenn man den Inhalt einfacher in einzelne Variablen entpacken könnte. Das geht so:
name,age,subject = student
print(name)
print(age)
print(subject)
# Ausgabe:
# Max Müller
# 22
# Informatik
# Achtung: dieses Entpacken funktioniert nur,wenn genausoviele Variablen haben,wie der Tupel Felder hat. Man kann
# z.B. nicht einen Tupel mit 4 Rückgabewerten in 3 Variablen entpacken

# Es kommt mitunter vor,dass man in einer Funktion mehrere Werte an die ursprüngliche aufrufende Stelle zurückgeben
# will.Eigentlich kann Python aber immer nur einen Rückgabewert zurückgeben. Das umgehen wir,indem wir die
# zurückzugebenden Werte einfach in ein Tupel "verpacken" und so die Limitierung auf einen Rückgabewert umgehen.

def get_student():
        return ("Rückgabewert1","Rückgabewert2","Rückgabewert3")

name,age,subject = get_student()
print(name)
print(age)
print(subject)
# Ausgabe
# Rückgabewert1
# Rückgabewert2
# Rückgabewert3

# Man kann auch Students in eine Liste packen und dann ausgeben
students = [("Max Müller",22),("Monika Mustermann",43),("Marco Jahn",50)] # eine Liste mit 3 einzelnen Tupels wurde
# erzeugt

for student in students: #eine For-Schleife ruft die Inhalte der Liste nacheinander ab
    print(student) #und gibt den aktuellen Wert zurück
#Ausgabe:
#('Max Müller', 22)
#('Monika Mustermann', 43)
#('Marco Jahn', 50)
