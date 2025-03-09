"""Wir wissen nun,wie man den Inhalt aus einer Datei lesen kann. Nun lernen wir,wie man etwas in eine Datei schreibt"""

file = open("schreiben.txt", "w")  # ein Objekt wird angelegt, in dem die zu schreibende Textdatei drinliegt, gemeinsam mit dem Befehl, dass in die Datei geschrieben wird
file.write("Marco")  # es wird etwas in die Datei geschrieben
file.write("Marco")  # es wird erneut etwas in die Datei geschrieben
file.close()  # die Datei wird nach dem Schreiben geschlossen

# beim Öffnen der Datei sehen wir nun diesen Inhalt:
# MarcoMarco
# Indem wir in den zu schreibenden Teil auch noch das Steuerzeichen für den Zeilenumbruch einbauen, können wir den 2.Eintrag in eine neue Datei packen:

file = open("schreiben.txt", "w")
file.write("Marco" + "\n")  # es wird etwas in die Datei geschrieben und ein Steuerzeichen angehängt
file.write("Marco")  # es wird erneut etwas in die Datei geschrieben
file.close()  # die Datei wird nach dem Schreiben geschlossen
# beim Öffnen der Datei sehen wir nun diesen Inhalt:
# Marco
# Marco

# Man kann z.B. auch Inhalte einer Liste übernehmen
students = ["Max", "Monika", "Petra", "Thomas"] # Die Liste wird angelegt
file = open("schreiben.txt", "w") # Die Datei wird zum schreiben geöffnet
for i in students: #für jeden Eintrag in der Liste
    file.write(i + "\n") # schreibe den Eintrag in die Liste und ergänze ein Steuerzeichen für den Zeilenumbruch
file.close()  # die Datei wird nach dem Schreiben geschlossen

# Inhalt der Textdatei ist nun
# Max
# Monika
# Petra
# Thomas

# Beim öffnen der Datei würde jedesmal der Inhalt überschrieben. Wenn wir stattdessen Inhalte anhängen wollen, können wir statt dem "w" den Schreibmodus "Append" benutzen:
students = ["Max", "Monika", "Petra", "Thomas"] # Die Liste wird angelegt
file = open("schreiben.txt", "a") # Die Datei wird zum schreiben geöffnet
for i in students: #für jeden Eintrag in der Liste
    file.write(i + "\n") # schreibe den Eintrag in die Liste und ergänze ein Steuerzeichen für den Zeilenumbruch
file.close()  # die Datei wird nach dem Schreiben geschlossen
