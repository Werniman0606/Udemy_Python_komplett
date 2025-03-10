"""Wenn eine Datei geöffnet wird,muss sie auch wieder geschlossen werden. Im Normalfall wird das durch file.close() übernommen. Wenn
das Programm aber vorher aus irgendeinem Grund abgebrochen wird, bleibt die Datei geöffnet, was zu Problemen führt"""

# Bisher haben wir das Programm so geschrieben:
file = open("schreiben.txt", "w")  # ein Objekt wird angelegt, in dem die zu schreibende Textdatei drinliegt, gemeinsam mit dem Befehl, dass in die Datei geschrieben wird
file.write("Marco")  # es wird etwas in die Datei geschrieben
file.write("Marco")  # es wird erneut etwas in die Datei geschrieben
file.close()  # die Datei wird nach dem Schreiben geschlossen

# Es gibt aber einen Weg, wie sich Python automatisch drum kümmert,dass die Datei geschlossen wird. Dazu nutzen wir das With Construct,
# welches file.close() überflüssig macht. Künftig schreiben wir also

with open("schreiben.txt","a") as file:
    file.write("Marco")  # es wird etwas in die Datei geschrieben
    file.write("Marco")  # es wird erneut etwas in die Datei geschrieben
