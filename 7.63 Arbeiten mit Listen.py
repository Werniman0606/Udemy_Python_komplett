# Wir wissen bereits, was Listen sind. Aber wie kriegen wir zum Beispiel raus,welches die ersten 10 Teilnehmer sind ? Oder die letzten 10 ?

students = ["Peter", "Paul", "Mary", "Joseph", "Jesus"]  # eine Liste namens students wird angelegt und befüllt

last_student = students.pop()  # Der Pop-Befehl löscht den letzten Eintrag in der Liste. Im vorliegenden Fall wird
# dieser Eintrag aber erst noch in eine Liste gepackt
print(last_student)
print(students)
# Ausgabe:
# Jesus
# ['Peter', 'Paul', 'Mary', 'Joseph'] Wie wir sehen,fehlt der letzte Eintrag

# Man kann aber auch 2 Listen zu einer verknüpfen

students = ["Peter", "Paul", "Mary", "Joseph", "Jesus"] + ["Petrus"]
print(students)  # Ausgabe: ['Peter', 'Paul', 'Mary', 'Joseph', 'Jesus', 'Petrus']

# mit dem Befehl del in Kombination mit einem Index kann man bestimmte Einträge löschen

del students[3]  # löscht den 4.Eintrag in der Liste (dran denken: es wird von 0 an gezählt,d.h. der Index 3 ist der
# 4.Eintrag
print(students)  # der Eintrag "Joseph" fehlt

# man kann aber auch direkt einen Eintrag löschen,wenn man z.B. den Index nicht kennt. Hierzu nutzt man aber nicht
# den del-Befehl,sondern den befehl remove
students.remove("Paul")
print(students)  # der Eintrag "Paul" fehlt
