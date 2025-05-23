# Warum nutzen wir private Eigenschaften und Methoden?
# In der Objektorientierten Programmierung (OOP) möchten wir oft sicherstellen,
# dass die internen Daten eines Objekts (seine Eigenschaften) nur auf kontrollierte Weise
# verändert werden können. Das nennt man Kapselung.
# Hier zeigen wir ein Problem und verschiedene Lösungsansätze dafür.

# --- Teil 1: Das Problem - Direkter Zugriff auf Attribute ---

class Student():
    # Der Konstruktor: Diese Methode wird immer aufgerufen, wenn du ein neues Student-Objekt erstellst.
    def __init__(self, firstname, lastname):
        # Hier werden die empfangenen Werte (Vorname, Nachname) den Instanzvariablen zugewiesen.
        # Diese Variablen sind aktuell "öffentlich", was bedeutet, dass du von außen direkt darauf zugreifen
        # und sie ändern kannst.
        self.firstname = firstname
        self.lastname = lastname
        # Das Semester wird mit einem Standardwert von 1 initialisiert. Auch 'term' ist öffentlich.
        self.term = 1

    # Eine Methode, um das Semester hochzuzählen.
    def increase_term(self):
        # Wir wollen verhindern, dass das Semester über 9 steigt.
        # Wenn es schon 9 oder höher ist, beenden wir die Methode einfach.
        if self.term >= 9:
            return
        # Andernfalls wird das Semester um 1 erhöht.
        self.term = self.term + 1 # Oder kürzer: self.term += 1

    # Eine Methode, um den vollen Namen und das aktuelle Semester auszugeben.
    def name(self):
        # Wir nutzen einen F-String für eine sauberere und modernere Ausgabe.
        # F-Strings erlauben es, Variablen direkt in geschweiften Klammern {} in den String einzufügen.
        print(f"{self.firstname} {self.lastname} (Semester: {self.term})")


# Erstellen einer neuen Instanz (eines Objekts) der Klasse Student.
# Erik Mustermann ist jetzt ein konkreter Student, basierend auf unserer Klasse.
erik = Student("Erik", "Mustermann")

# Wir rufen die Methode 'increase_term' mehrmals auf, um das Semester kontrolliert zu erhöhen.
# Jede dieser Aufrufe erhöht das Semester um eins, bis das Limit von 9 erreicht ist.
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term() # Dieser und weitere Aufrufe haben keinen Effekt, da 'term' bereits 9 ist.
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()

# Ausgabe des Studentennamens und des Semesters.
# Wir sehen, dass das Semester durch unsere Methode korrekt bei maximal 9 bleibt.
erik.name()  # Ausgabe: Erik Mustermann (Semester: 9)

# --- Das Problem: Direkte Manipulation ---
# Obwohl unsere Methode 'increase_term' eine Logik hat, die das Semester auf 9 begrenzt,
# können wir das Attribut 'term' immer noch direkt von außen manipulieren, weil es öffentlich ist.
# Das untergräbt unsere beabsichtigte Kontrolle über die Daten.
erik.term = 100 # Hier überschreiben wir das Semester einfach manuell!
erik.name()  # Ausgabe: Erik Mustermann (Semester: 100) - Das ist unerwünscht!


# --- Teil 2: Lösungen für Kapselung ---

# Es gibt in Python zwei gängige Ansätze, um den direkten Zugriff auf Attribute zu steuern:

# a) Die Konvention des einzelnen Unterstrichs (_):
# Wenn du einem Attributnamen einen einzelnen Unterstrich voranstellst, z.B. `_term`,
# ist das ein starker Hinweis an andere Programmierer: "Dieses Attribut ist intern und
# sollte von außen nicht direkt geändert werden." Es ist KEINE technische Barriere,
# sondern eine Vereinbarung unter Entwicklern. Man spricht hier oft von "geschützten" Attributen.
# Du könntest immer noch `erik._term = 100` schreiben, aber es wäre schlechter Stil.

# b) Der doppelte Unterstrich (__) für "Privatheit" (Name Mangling):
# Wenn du einem Attributnamen ZWEI Unterstriche voranstellst (z.B. `__term`),
# macht Python den Zugriff von außen schwieriger. Man nennt das "Name Mangling".
# Python ändert den Namen des Attributs intern, um Kollisionen zu vermeiden und den direkten Zugriff
# von außerhalb der Klasse zu erschweren.

class Student():
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        # Jetzt ist '__term' ein "privates" Attribut. Python benennt es intern um
        # (z.B. zu '_Student__term'), um den direkten Zugriff von außen zu verhindern.
        self.__term = 1

    def increase_term(self):
        # Auch hier verwenden wir '__term', da wir uns innerhalb der Klasse befinden.
        if self.__term >= 9:
            return
        self.__term += 1 # Kürzere Schreibweise

    def name(self):
        # Wir können von innerhalb der Klasse auf '__term' zugreifen.
        print(f"{self.firstname} {self.lastname} (Semester: {self.__term})")


erik = Student("Erik", "Mustermann")

# Wir erhöhen das Semester wieder, um zu zeigen, dass die interne Logik noch funktioniert.
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.name()  # Ausgabe: Erik Mustermann (Semester: 9)

# Versuch, das "private" Attribut von außen zu ändern:
# Obwohl es so aussieht, als würden wir __term setzen, erstellen wir hier tatsächlich
# ein NEUES, öffentliches Attribut namens '__term' auf dem 'erik'-Objekt.
# Das ursprüngliche private '__term' (intern umbenannt zu '_Student__term') bleibt unberührt.
erik.__term = 100
erik.name()  # Ausgabe: Erik Mustermann (Semester: 9) - Der Wert ist immer noch 9!
# Wie wir sehen, bleibt das Semester weiter bei 9, weil der doppelte Unterstrich verhindert,
# dass die eigentliche Klassenvariable `__term` von außen verändert wird.
# Das neue Attribut `erik.__term` hat keinen Einfluss auf das interne `__term` der Klasse.


# --- Teil 3: Kontrollierter Zugriff auf private Attribute (Getter) ---

# Aber was machen wir, wenn wir von außen auf den Inhalt dieser privaten Variable `__term`
# zugreifen wollen – aber nur auf kontrollierte Weise?
# Dafür verwenden wir spezielle Methoden, sogenannte "Getter".

# Ein Getter ist eine Methode, die den Wert eines privaten Attributs zurückgibt.
# Ein Setter (hier nicht gezeigt, aber oft in Kombination genutzt) wäre eine Methode,
# die den Wert eines privaten Attributs setzt, oft mit Validierung.

class Student():
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.__term = 1

    def increase_term(self):
        if self.__term >= 9:
            return
        self.__term += 1

    # Diese Methode ist ein "Getter". Sie erlaubt es, den aktuellen Wert
    # des privaten Attributs '__term' von außen auszulesen.
    # Sie stellt eine kontrollierte Schnittstelle dar, um auf den Wert zuzugreifen.
    def get_term(self):
        return self.__term

    def name(self):
        print(f"{self.firstname} {self.lastname} (Semester: {self.__term})")


erik = Student("Erik", "Mustermann")
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term()
erik.increase_term() # Mehrfache Aufrufe bis 9
erik.increase_term()
erik.name()  # Ausgabe: Erik Mustermann (Semester: 9)

# Der Versuch, '__term' direkt zu manipulieren, funktioniert weiterhin nicht für das interne Attribut.
erik.__term = 100
erik.name()  # Ausgabe: Erik Mustermann (Semester: 9)

# --- Nutzung des Getters ---
# Wir rufen die 'get_term()'-Methode auf, um den aktuellen Wert von '__term' zu erhalten.
print(f"Aktuelles Semester über Getter: {erik.get_term()}")  # Ausgabe: Aktuelles Semester über Getter: 9


# --- Private Methoden ---
# Wir können auch Methoden mit der gleichen Art und Weise - dem Voranstellen von 2 Unterstrichen -
# auf "privat" stellen (z.B. `__interne_berechnung()`).
# Sie lässt sich dann von außen nicht mehr direkt aufrufen, aus der Klassendefinition hingegen schon.
# Das ist nützlich für Hilfsfunktionen, die nur für die interne Logik der Klasse relevant sind.