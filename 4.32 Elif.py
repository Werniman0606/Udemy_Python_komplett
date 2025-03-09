"""Man könnte den Status einer Variablen prüfen,indem man mehrere If-Abfragen ineinander verschachtelt"""

currency = "€"  # die Variable wird definiert

if currency == "$":  # wenn die Variable Dollar ist,
    print("US-Dollar")  # dann gib das hier aus
else:  # andernfalls wird gecheckt
    if currency == "Y":  # ob die Variable das Zeichen für Yen enthält und wenn ja
        print("Japanischer Yen")  # wird dieser Text ausgegeben
    else:  # falls nicht, wird wieder weiter gecheckt
        if currency == "€":  # ob die Variable vielleicht das Eurozeichen enthält
            print("Euro")  # und wenn ja, wird der Text ausgegeben
# Das bedeutet,dass die Abfragen ineinander verschachtelt sind,was sie sehr schwer lesbar macht

# Besser wären Elif-Abfragen
if currency == "$":  # wenn die Variable Dollar ist,
    print("US-Dollar")  # dann gib das hier aus
elif currency == "Y":  # ob die Variable das Zeichen für Yen enthält und wenn ja
    print("Japanischer Yen")  # wird dieser Text ausgegeben
elif currency == "€":  # ob die Variable vielleicht das Eurozeichen enthält
    print("Euro")  # und wenn ja, wird der Text ausgegeben

# wie man sieht, ist das schon deutlich übersichtlicher, weil die Else-Befehle mit den If-Befehlen verknüpft werden (zu "Elif" statt "Else: if"
