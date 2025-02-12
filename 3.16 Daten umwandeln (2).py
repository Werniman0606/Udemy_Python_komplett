students = ["Max", "Monika", "Peter", "Heinz"]  # Wir legen eine Liste mit Namen an
print(students)  # Ausgabe: ['Max', 'Monika', 'Peter', 'Heinz']

# Diese Liste wollen wir nun mit Komma getrennt ausgeben. Das können wir tun, indem wir einen sogenannten Seperator benutzten.
print(",".join(students))  # Bedeutet benutze das Komma als Separator und verbinde damit die Liste "Students". Ausgabe:
# Max,Monika,Peter,Heinz
# Man könnte diese Ausgabe (welche ein String ist) auch wieder zerteilen und in eine neue Liste packen. Dazu packen wir die Ausgabe
# erstmal in eine Variable:
studentennamen = ",".join(
    students)  # Die Liste wird in einen String mit Kommatrennung gewandelt und in die Variable "Studentennamen" gepackt
print(studentennamen)  # der String wird ausgegeben

print(studentennamen.split(","))  # Ausgabe: eine Liste mit den Namen der Studenten
Namen = studentennamen.split(",")  # Die Ausgabe des Splitbefehls ist eine Liste und bekommt einen Listennamen
print(Namen)  # Die neue Liste wird ausgegeben
# -------------------------------
# Man könnte das auch weiterspielen:
a = "Am Samstag Abend lege ich mich aufs Sofa und schlummere"  # wir legen einen String in eine Variable
print(len(a.split(" ")))  # dieser Befehl würde den Satz an jedem Lehrzeichen in einen Listeneintrag splitten und anschließend zählen,
# wieviele Einträge die Liste hat,d.h. die Worte werden gezählt.
