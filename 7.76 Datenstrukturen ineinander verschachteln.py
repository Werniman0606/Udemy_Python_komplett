# In Python ist es erlaubt, Listen ineinander zu verschachteln, was uns erlaubt, z.B. eine Matrix zu modellieren.
# In dieser Lektion lernen wir,wie man Listen ineinander verschachtelt und auf die Elemente zugreift.
liste = [
    ["Berlin", "München", "Köln"],
    ["Budapest", "Pecs", "Sopron"]

]

# für mehrdimensionale Listen ist die zeilenweise getrennte Schreibweise beim erstellen einfacher zu überblicken.
# Wir haben soeben eine mehrdimensionale Liste erzeugt. Wir können auf eine der enthaltenen Liste auf die gewohnte
# Weise zugreifen
print(liste[0])
# Ausgabe: ['Berlin', 'München', 'Köln']

# Indem wir eine weitere eckige Klammer angeben, können wir festlegen, dass wir auf das 2.Element der 1.Liste
# zugreifen wollen
print(liste[0][1])
# Ausgabe: München
