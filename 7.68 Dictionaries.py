# Dictionaries erlauben es, Wertezuordnungen zu speichern. So wird z.B. einem Nachnamen eine Telefonnummer zugeordnet
# Man kann nachträglich Elemente ändern, entfernen oder hinzufügen
# Dictionaries werden nicht mit eckigen Klammern (wie Listen), sondern mit geschweiften Klammern geschrieben
d = {"Berlin": "BER", "Helsinki": "HEL", "Saigon": "SGN"}  # Dem Wert Berlin wird die Abkürzung BER zugeordnet usw.
print(d)  # Ausgabe: {'Berlin': 'BER', 'Helsinki': 'HEL', 'Saigon': 'SGN'}
print(d["Helsinki"])  # Ausgabe: "HEL, Es wird der dem Wert Helsinki zugeordnete Partnerwert ausgegeben

# Wenn man neue Werte hinzufügen will,ist das ziemlich einfach.
d["London"] = "LON"
print(d)  # Ausgabe: {'Berlin': 'BER', 'Helsinki': 'HEL', 'Saigon': 'SGN', 'London': 'LON'}

# Mit dem bereits bekannten del-Befehl kann man aber auch  Elemente und ihre Zuordnung löschen
del d["Helsinki"]
print(d)  # Ausgabe: {'Berlin': 'BER', 'Saigon': 'SGN', 'London': 'LON'} Helsinki wurde gelöscht

# Um Werte auszugeben,kann man entweder mit eckigen Klammern oder der Get-Funktion arbeiten:
print(d["Saigon"]) # Ausgabe: SGN
print(d.get("Saigon")) # Ausgabe: SGN

#Warum sollte man besser mit der ersteren Methode mit den eckigen Klammern arbeiten ?
# Weil erstere Methode einen KeyError ausgibt,wenn es den gesuchten Begriff nicht gibt,so dass man Fehler schneller
# bemerkt, während die 2.Methode einfach stur weiterläuft.
s