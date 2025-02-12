"""In dieser Lektion geht es um Booleans und AND/OR-Abfragen,welches ermöglicht, Bedingungen zu verknüpfen"""
# Bisher hätten wir das so geschrieben:

age = 34  # alter wird in ihre Variable gepackt
if age >= 30:  # wenn alter größergleich 30, führe nächste Zeile aus
    if age <= 39:  # wenn alter kleinergleich 39 ist, führe nächste Zeile aus
        print("Die Person ist ihren 30ern!")  # gib Text aus. Ausgabe: Die Person ist ihren 30ern!
# Die If-Abfragen sind also verschachtelt.


# Nun verknüpfen wir die Abfrage
if age >= 30 and age <= 39: # wenn die erste Bedingung erfüllt ist UND die 2.Bedingung erfüllt ist, dann führe nächste Zeile aus
     print("Die Person ist ihren 30ern!")


#es gibt auch noch den OR-Operator
age = 17 #Variable wird neu befüllt
if age<30 or age>=40:  #Es wird geprüft, ob die Person unter 30 oder über 40 ist
    print("Die Person ist NICHT in ihren 30ern")


#man kann aber auch Bool-Variablen vergleichen
if True:
    print("Die If-Abfrage wurde ausgeführt")
# Diese Abfrage macht relativ wenig sinn, weil im Grunde nur eine Print-Anweisung in einer Bedingung ausgeführt wurde,ohne dass überhaupt
# wirklich was geprüft wurde. D.h. if True würde sofort den Kommandoblock ausführen

#Man kann es aber sinnvoller einsetzen:
age = 25
above20 = age >=20  #es würde geprüft,ob der Wert von age mindestens 20 ist. Der Bool-Rückgabewert wird in die Variable above20 gesteckt.
print(above20) # Ausgabe: True
if above20: #Wenn der Inhalt der Bool-Variable True ist, führe den Kommandoblock aus. Wenn das = fehlt, heißt das,dass die If-Anweisung
    # prüft,ob die Variable True ist.
    print("Das alter ist über 20")



