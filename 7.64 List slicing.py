students = ["Peter", "Paul", "Mary", "Joseph", "Jesus"]

# will man auf das letzte Objekt zugreifen,kann man mit negativen Indizes arbeiten. Allerdings fängt dann die
# Zählweise nicht mit 0 an, sondern mit - 1.

print(students[-1]) # Ausgabe: Jesus
print(students[-3]) # Ausgabe: Mary

# Beim List Slicing wird einfach ein Teil einer Liste ausgegeben. Das wird gemacht,indem wir beim Index keinen festen
# Wert eingeben,sondern einen Bereich. Die Ausgabe beginnt immer mit dem Startwert, endet aber VOR dem Endwert
print(students[1:4]) # Ausgabe: ['Paul', 'Mary', 'Joseph']
# wir sehen,dass Paul noch mit ausgeben wird, Jesus als Element mit dem Index 4 jedoch nicht mehr

# Wenn man einen Wert weglässt, werden alle Inhalte ab/bis zum betreffenden Wert angezeigt
print(students[1:]) # Ausgabe: ['Paul', 'Mary', 'Joseph', 'Jesus'] Es fehlt "Peter",weil dieser Index 0 hat
print(students[:4]) # Ausgabe: ['Peter', 'Paul', 'Mary', 'Joseph'] # es fehlt Jesus,weil das letzte Element
# ausgeklammert wird

#so man die Anzahl an Einträgen nicht kennt,kann man auch einfach Index-Angaben von hinten machen. Wenn
# beispielsweise bis vor den letzten Eintrag aufgelistet werden soll:
print(students[0:-1]) # Ausgabe: ['Peter', 'Paul', 'Mary', 'Joseph'] Es fehlt "Jesus",weil dieser Index -1 hat

# List Slicing funktioniert auch mit Strings
print("Hallo Welt"[0:5]) # Ausgabe: "Hallo" Es wird also vor Index 5 aufgehört
print("Hallo Welt"[-4:]) # Ausgabe: "Welt", d.h. es wird vom viertletzten Zeichen bis zum Ende ausgegeben



