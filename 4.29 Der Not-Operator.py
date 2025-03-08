# Nun wollen wir lernen, wie wir prüfen, ob es einen Eintrag NICHT gibt. Dazu gibts den Not-Operator. Diesen kann man auf unterschiedliche Art einsetzen

names = ["Max", "Moritz", "Fritzchen"]  # eine Liste wird angelegt

# auf diese Art würde direkt geprüft, ob der Name Monika NICHT in der Liste vorhanden ist.
if "Monika" not in names:
    print("Den Namen Monika gibts nicht in der Liste")

# auf diese Art würde geprüft, ob der Name Monika in der liste drin ist und das Ergebnis würde umgekehrt.
# D.h. das "Monika" in Names würde ein "False" zurückgeben,weil es den Namen nicht gibt. Das vorangestellte not würde
# das False jedoch in ein True umwandeln, womit die Bedingung erfüllt ist und die Printanweisung ausgeführt ist

if not "Monika" in names:
    print("Den Namen Monika gibts nicht in der Liste")

# in der Praxis funktionieren beide Varianten,die erstere ist aber einfacher zu lesen und daher meit praktikabler
