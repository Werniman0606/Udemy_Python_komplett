file = open("lesen.txt", "r")  # eine Variable wird mit der Datei lesen.txt gefüllt, die zum lesen ("r") geöffnet wird
for i in file:
    print(i)
# Ausgabe:
# Hallo Welt!
#
# Ich bin eine neue Datei und soll nun gelesen werden!

"""Warum wird eine Leerzeile zwischen den einzelnen Zeilen ausgegeben,obwohl in der Textdatei keine solche drin ist ? 
Nun,das liegt daran, dass es Steuerzeichen gibt, die aber normalerweise in Textdateien nicht da sind. Eine Zeile endet also immer mit einem
Zeichen für den Zeilenumbruch, der so aussieht: "\n". Die Zeile "Hallo Welt!" endet also nicht mit dem Ausrufezeichen,sondern mit dem Zeilenumbruch \n. Und das merkt Python und 
führt den Textumbruch aus. Aus diesem Grund ist der Zeilenumbruch vorhanden. Ein neuer Print-Befehl sorgt zusätzlich für einen Zeilenumbruch,was im Endeffekt die "überflüssige"
Leerzeile ergibt. Man kann diese Steuerzeichen bei der Ausgabe entfernen,indem wir der eingelesenen Zeile, die in der Variablen I vorliegt, den Befehl strip() anhängen, wodurch
überflüssige Leerzeichen und Zeilenumbrücke entfernt werden. Das sieht dann insgesamt so aus:
"""

file = open("lesen.txt", "r")  # Die Datei wird geöffnet
for i in file:  # die einzelnen Zeilen werden aus der Datei gelesen und in die Variable i gepackt
    print(i.strip())  # die einzelen Zeilen werden um überflüssige Leerzeilen und Steuerzeichen bereinigt ausgegeben
# Ausgabe
# Hallo Welt!
# Ich bin eine neue Datei und soll nun gelesen werden
