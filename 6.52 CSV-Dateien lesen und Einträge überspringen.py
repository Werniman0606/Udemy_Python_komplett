""" In dieser Lektion lernen wir,wie wir die Datei lesen und Einträge überspringen."""

# Das folgende Programm kennen wir schon aus der letzten Lektion
with open("datei.csv") as file:  # Datei wird geöffnet. Wir verwenden with,damit sie sich nach Nutzung automatisch schließt
    for line in file:  # für jede Zeile in dieser Datei
        data = line.strip().split(";")  # die Datei wird bereinigt und gesplittet und in eine Liste verpackt
        print(data[0] + ": " + data[1])

# Nun möchten wir alle Einträge ausgeben, wo in der 3.Spalte ein "BER" steht. Wir wissen,dass die gelesenen Einträge in eine Liste namens
# 'data" gespeichert wurden und als Trennzeichen das Semikolon benutzt wurde.D.h. wir können auf die einzenen Teile über ihren Indexwert
# zugreifen
with open("datei.csv") as file:  # Datei wird geöffnet. Wir verwenden with,damit sie sich nach Nutzung automatisch schließt
    for line in file:  # für jede Zeile in dieser Datei
        data = line.strip().split(";")  # die Datei wird bereinigt und gesplittet und in eine Liste verpackt
        if data[2] == "BER":
            print(data[0] + ": " + data[1])
            #Ausgabe: Berlin: 3000000

# Aber was machen wir,wenn wir alle Städte finden wollen, die mehr als 2 Mio Einwohner haben ? Nun, nach unserem bisherigen Wissensstand
# würden wir sowas hier schreiben
# with open("datei.csv") as file:  # Datei wird geöffnet. Wir verwenden with,damit sie sich nach Nutzung automatisch schließt
#    for line in file:  # für jede Zeile in dieser Datei
#       data = line.strip().split(";")  # die Datei wird bereinigt und gesplittet und in eine Liste verpackt
#       if data[1] >= 2000000:
#           print(data[0] + ": " + data[1])
# Doch das ergibt einen Type Error,weil Vergleiche mit >= nicht erlaubt sind in Strings (d.h. die eingelegesenen Daten liegen als Strg vor.
# Das umgehen wir,indem wir den Text in eine Zahl umwandeln. Das geht, wie wir bereits wissen, mit dem Cast-Befehl
with open("datei.csv") as file:  # Datei wird geöffnet. Wir verwenden with,damit sie sich nach Nutzung automatisch schließt
    for line in file:  # für jede Zeile in dieser Datei
       data = line.strip().split(";")  # die Datei wird bereinigt und gesplittet und in eine Liste verpackt
       if int(data[1]) >= 2000000: # das vorangestellte int wandelt den Strg-Inhalt des Feldes in eine Zahl um, die dann vergleichbar ist
           print(data[0] + ": " + data[1])
            # Ausgabe:
            # Berlin: 3000000
            # Budapest: 2000000

# Den gleichen Effekt kann man aber auch erreichen,indem man eine Ausgabe bewirkt, aber die Einträge überspringt, die kleiner als 2 Mio
# sind.
with open("datei.csv") as file:  # Datei wird geöffnet. Wir verwenden with,damit sie sich nach Nutzung automatisch schließt
    for line in file:  # für jede Zeile in dieser Datei
       data = line.strip().split(";")  # die Datei wird bereinigt und gesplittet und in eine Liste verpackt
       if int(data[1]) < 2000000: # das vorangestellte int wandelt den Strg-Inhalt des Feldes in eine Zahl um, die dann vergleichbar ist
            continue
       print(data)
        # Ausgabe:
        # Berlin: 3000000
        # Budapest: 2000000

