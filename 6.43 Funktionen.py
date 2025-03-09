""" In Funktionen können wir wiederkehrende Befehlsblöcke definieren,um sie später immer wiederverwenden zu können."""


def multi_print():  # Die Funktion multi_print wird erzeugt. Ihr wird kein Parameter mitgegeben. Die Klammern sind zwingend nötig.
    print("Hallo Welt")  # diese 2 Zeilen sollen ausgegeben werden
    print("Hello World")

multi_print()  # die erzeugte Funktion wird ausgeführt
# Ausgabe.
# Hallo Welt
# Hello World


# Man kann aber auch beim Aufruf der Funktion Parameter mitgeben, die innerhalb der Funktion weiterbenutzt werden kann.
def multi_print2(name):
    print(name)

multi_print2("Fritzchen")
# Ausgabe:
# Fritzchen
