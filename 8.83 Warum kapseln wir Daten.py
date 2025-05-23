# --- Lektion: Warum kapseln wir Daten? ---
# In dieser Lektion lernen wir, warum es wichtig ist, Daten in der Objektorientierten Programmierung (OOP)
# zu "kapseln" und wie das mit Python funktioniert. Kapselung bedeutet, die internen Details eines Objekts
# zu verbergen und den Zugriff darauf nur über klar definierte Schnittstellen (Methoden) zu erlauben.

# Stellen wir uns vor, wir erstellen ein digitales Telefonbuch:

# --- Teil 1: Das Problem - Fehlende Kapselung (direkter Zugriff) ---

class PhoneBook():
    # Der Konstruktor: Diese Methode wird jedes Mal ausgeführt, wenn du ein neues PhoneBook-Objekt erstellst.
    def __init__(self):
        # Hier wird ein leeres Dictionary namens 'entries' erstellt.
        # Aktuell ist dieses Dictionary "öffentlich", was bedeutet, dass es von außerhalb
        # der Klasse direkt eingesehen und sogar verändert werden kann.
        self.entries = {}

    # Die 'add'-Methode: Fügt einen neuen Eintrag zum Telefonbuch hinzu.
    # Beim Aufruf dieser Methode werden der 'name' und die 'phone_number' übergeben.
    def add(self, name, phone_number):
        # Der empfangene Name wird als Schlüssel und die Telefonnummer als Wert in das Dictionary eingefügt.
        self.entries[name] = phone_number

# Erzeugen einer neuen Instanz (eines Objekts) der Klasse PhoneBook.
book = PhoneBook()

# Hinzufügen von Einträgen zum Telefonbuch über die 'add'-Methode.
book.add("Jahn", "+493678137965")
book.add("Pabst", "+493670561420")

# Das Problem: Direkter Zugriff auf interne Daten
# Weil das 'entries'-Dictionary öffentlich ist, können wir direkt darauf zugreifen
# und es sogar unerwartet manipulieren, was zu Dateninkonsistenzen führen kann.
print("Direkter Zugriff auf das Dictionary (unerwünscht):", book.entries)
# Ausgabe: {'Jahn': '+493678137965', 'Pabst': '+493670561420'}

# Man könnte sogar das gesamte Dictionary von außen überschreiben oder Einträge löschen!
book.entries = {"Frank": "+49123456789"} # Ohne Kapselung kann man das Telefonbuch einfach manipulieren!
print("Nach unerlaubter Manipulation:", book.entries)
# Dies zeigt das Risiko: Die interne Datenstruktur (das Dictionary) ist ungeschützt.

# --- ---

# --- Teil 2: Die Lösung - Datenkapselung mit privaten Attributen ---

# Um solche unerwünschten Manipulationen zu verhindern und die Kontrolle über die Daten zu behalten,
# kapseln wir das interne Dictionary. In Python erreichen wir das, indem wir dem Attributnamen
# zwei Unterstriche (__) voranstellen.

class PhoneBook():
    def __init__(self):
        # Das Dictionary '__entries' wird jetzt als "privat" deklariert.
        # Python führt hier "Name Mangling" durch (ändert den Namen intern z.B. zu '_PhoneBook__entries'),
        # was den direkten Zugriff von außen erschwert und Kapselung fördert.
        self.__entries = {}

    def add(self, name, phone_number):
        # Die 'add'-Methode kann weiterhin intern auf '__entries' zugreifen.
        self.__entries[name] = phone_number

    # Eine "Getter"-Methode: Ermöglicht den kontrollierten Zugriff auf einzelne Einträge.
    # Von außen können wir jetzt nicht mehr das gesamte Dictionary sehen, sondern nur
    # gezielt nach einem Namen fragen.
    def get(self, name):
        # Überprüfen, ob der Name im privaten Dictionary existiert.
        if name in self.__entries:
            # Gibt die zum Namen gehörige Telefonnummer zurück.
            return self.__entries[name]
        else:
            # Wenn der Name nicht gefunden wird, geben wir 'None' zurück (was "nichts" bedeutet).
            return None

    # Optional: Eine Methode, um die Anzahl der Einträge zu erfahren, ohne das ganze Dictionary preiszugeben.
    def size(self):
        return len(self.__entries)

# Erzeugen einer neuen Instanz des gekapselten Telefonbuchs.
book_encapsulated = PhoneBook()

# Hinzufügen von Einträgen. Diese Funktion funktioniert weiterhin wie erwartet.
book_encapsulated.add("Jahn", "+493678137965")
book_encapsulated.add("Pabst", "+493670561420")

# Versuch des direkten Zugriffs auf das gekapselte Dictionary:
# Dies würde einen 'AttributeError' verursachen, weil '__entries' nicht direkt von außen sichtbar ist.
# Oder, wie in der vorherigen Lektion besprochen, würde ein NEUES, öffentliches Attribut 'book_encapsulated.__entries' erstellt,
# das nichts mit dem internen, privaten Dictionary zu tun hat.
# print(book_encapsulated.__entries) # <-- Dies würde einen Fehler verursachen oder nicht das gewünschte Ergebnis liefern!

# Kontrollierter Zugriff über die 'get'-Methode:
print("Telefonnummer von Jahn (über Getter):", book_encapsulated.get("Jahn")) # Ausgabe: +493678137965
print("Telefonnummer von Meier (nicht vorhanden):", book_encapsulated.get("Meier")) # Ausgabe: None

# Nutzung der optionalen 'size'-Methode:
print("Anzahl der Einträge im Telefonbuch:", book_encapsulated.size()) # Ausgabe: 2

# --- Fazit zur Kapselung ---
# Wie wir sehen, können wir in der zweiten Variante nicht einfach das gesamte Dictionary direkt ausgeben
# oder manipulieren, weil es "privat" (geKapselt) ist. Stattdessen können wir nur über
# die bereitgestellten Methoden (wie `add` oder `get`) mit den Daten interagieren.
# Dies schützt unsere Daten vor unerwarteten Änderungen und macht den Code robuster und sicherer.
# Es ist ein Kernprinzip der Objektorientierung, um die **Datenintegrität** zu gewährleisten.