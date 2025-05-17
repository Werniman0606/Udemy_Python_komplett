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

# Einfacher wäre es, wenn man