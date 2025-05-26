# --- Übungsaufgaben ---

# Aufgabe 1: Modelliere einen Würfel
# Erstelle eine Klasse `_Cube_`, mit der du einen Würfel modellierst.
# Die Würfel-Klasse soll als Eigenschaft die Länge einer Würfel-Seite besitzen.
# Darüber hinaus soll die Klasse auch zwei Methoden haben: die Methode `volume()`
# berechnet das Volumen und gibt es aus, die Methode `surface()` berechnet die Oberfläche und gibt es aus.


class Cube():
    """
    Diese Klasse modelliert einen Würfel und ermöglicht die Berechnung
    seines Volumens und seiner Oberfläche.
    """
    def __init__(self, side):
        """
        Der Konstruktor der Klasse `Cube`.
        Initialisiert eine neue Würfel-Instanz mit der gegebenen Seitenlänge.

        Args:
            side (float oder int): Die Länge einer Seite des Würfels.
        """
        # Der empfangene Parameter 'side' wird als Instanzvariable 'self.side' gespeichert.
        # Jede Würfel-Instanz hat ihre eigene Seitenlänge.
        self.side = side

    def surface(self):
        """
        Berechnet die Oberfläche des Würfels und gibt das Ergebnis aus.
        Formel: 6 * Seitenlänge^2
        """
        # Die Formel für die Oberfläche eines Würfels ist (Seitenlänge * Seitenlänge) * 6.
        print(self.side ** 2 * 6)

    def volume(self):
        """
        Berechnet das Volumen des Würfels und gibt das Ergebnis aus.
        Formel: Seitenlänge^3
        """
        # Die Formel für das Volumen eines Würfels ist Seitenlänge hoch 3.
        print(self.side ** 3)


# --- Test der Cube-Klasse ---
# Danach erzeugen wir eine Instanz deiner Cube-Klasse.
a = Cube(3)  # Eine Instanz mit dem Namen 'a' wird angelegt und die Seitenlänge 3 übergeben.
# Und testen die Methoden.
a.surface()  # Die Methode zur Berechnung der Oberfläche wird ausgeführt.
a.volume()   # Die Methode zur Berechnung des Volumens wird ausgeführt.


# ----------------------------------

# Aufgabe 2: Modelliere eine Kugel
# Die Kugel-Klasse soll als Eigenschaft den Radius übergeben bekommen.
# Zudem soll sie – ähnlich wie der Würfel – zwei Methoden haben:
# `surface()` um den Oberflächeninhalt zu berechnen, `volume()` um das Volumen zu berechnen.
# Damit du diese Berechnungen durchführen kannst, benötigst du die Kreiszahl Pi.
# Diese steht dir nach einem `import math` unter `math.pi` zur Verfügung.
# (Was der `import`-Befehl genau macht, schauen wir uns noch später im Kurs an).

# Die Formeln für den Oberflächeninhalt / das Volumen einer Kugel darfst du im Internet nachgucken.
#
import math # Importiert das 'math'-Modul, das mathematische Funktionen und Konstanten (wie Pi) enthält.


class Ball():
    """
    Diese Klasse modelliert eine Kugel und ermöglicht die Berechnung
    ihres Oberflächeninhalts und Volumens.
    """
    def __init__(self, radius):
        """
        Der Konstruktor der Klasse `Ball`.
        Initialisiert eine neue Kugel-Instanz mit dem gegebenen Radius.

        Args:
            radius (float oder int): Der Radius der Kugel.
        """
        self.radius = radius

    def surface(self):
        """
        Berechnet den Oberflächeninhalt der Kugel und gibt das Ergebnis aus.
        Formel: 4 * Pi * Radius^2
        """
        # Berechnet die Oberfläche der Kugel (4 * Pi * Radius hoch 2).
        print(4 * math.pi * self.radius ** 2)

    def volume(self):
        """
        Berechnet das Volumen der Kugel und gibt das Ergebnis aus.
        Formel: (4/3) * Pi * Radius^3
        """
        # Berechnet das Volumen der Kugel (4/3 * Pi * Radius hoch 3).
        print(4 / 3 * math.pi * self.radius ** 3)


# --- Test der Ball-Klasse ---
b = Ball(4) # Eine Instanz mit dem Namen 'b' wird angelegt und der Radius 4 übergeben.
# Und führen die Methoden aus.
b.surface()
b.volume()


# -------------------------
### Aufgabe 3: Modelliere ein Konto

# Erstelle die Konto-Klasse `_Account_` mit der Eigenschaft Kontostand `_credits_`!
# Diese Eigenschaft wird mit einem Startkapital initialisiert. Die Methode `display()`
# soll den aktuellen Kontostand ausgeben.

# Ergänze die Klasse `_Account_` um zwei Methoden (`pay_in()` zum Einzahlen, `withdraw()` zum Abheben),
# so dass du Geldbeträge einzahlen und abbuchen kannst, und der Kontostand entsprechend angepasst wird.
# Du sollst nur Geld abheben können, solange auch Geld auf dem Konto ist.
# Ein Dispo-Kredit wird nicht gewährt. In dem Fall soll eine Fehlermeldung ausgegeben werden,
# in der steht, wieviel Geld maximal abgebucht werden kann.
#

class Account():
    """
    Diese Klasse modelliert ein Bankkonto mit grundlegenden Funktionen
    wie Einzahlen, Abheben und Anzeigen des Kontostands.
    """
    def __init__(self, start):
        """
        Der Konstruktor der Klasse `Account`.
        Initialisiert ein neues Konto mit dem gegebenen Startguthaben.

        Args:
            start (float oder int): Das initiale Guthaben auf dem Konto.
        """
        # Der Konstruktor empfängt das Startguthaben und speichert es als Instanzvariable 'self.credits'.
        self.credits = start

    def display(self):
        """
        Gibt den aktuellen Kontostand des Kontos aus.
        """
        print(self.credits)

    def pay_in(self, money):
        """
        Zahlt einen bestimmten Betrag auf das Konto ein.

        Args:
            money (float oder int): Der Betrag, der eingezahlt werden soll.
        """
        # Die Methode zum Einzahlen addiert den einzuzahlenden Betrag zum aktuellen Kontostand hinzu.
        self.credits += money

    def withdraw(self, money):
        """
        Hebt einen bestimmten Betrag vom Konto ab, falls genügend Guthaben vorhanden ist.
        Verhindert eine Überziehung des Kontos.

        Args:
            money (float oder int): Der Betrag, der abgehoben werden soll.
        """
        # Die Methode prüft, ob das aktuelle Guthaben größer oder gleich dem abzuhebenden Betrag ist.
        if self.credits >= money:  # Wenn genug Guthaben vorhanden ist,
            # wird der abzuhebende Betrag vom Kontostand abgezogen.
            self.credits -= money
        else:  # Falls nicht genug Guthaben vorhanden ist,
            # wird eine Fehlermeldung ausgegeben, die den maximal abhebbaren Betrag anzeigt.
            print("Du kannst nur noch " + str(self.credits) + "€ abheben!")


# --- Test der Account-Klasse (Teil 1) ---
Kunde111 = Account(500)  # Eine Instanz mit dem Namen 'Kunde111' wird angelegt und das Startguthaben 500 übergeben.
Kunde111.display()  # Die Methode zur Ausgabe des Kontostands wird ausgeführt.
Kunde111.pay_in(40)  # Eine Einzahlung von 40€ wird getätigt.
Kunde111.display()  # Der aktualisierte Kontostand wird ausgegeben.
Kunde111.withdraw(25)  # Eine Abhebung von 25€ wird versucht.
Kunde111.display()  # Der aktualisierte Kontostand wird ausgegeben.
Kunde111.withdraw(600)  # Ein Abhebeversuch von 600€. Da das Konto nicht gedeckt ist,
# wird die Fehlermeldung mit dem maximal verfügbaren Betrag ausgegeben.


# -------------------------
# Bislang ist das Konto noch ungeschützt – wir brauchen eine PIN!
# Ergänze in der Klasse die Eigenschaft `_pin_`! So wie mit dem Startkapital
# soll das Konto auch mit einer PIN initialisiert werden. Von nun an muss man beim Geldabheben
# nicht nur den Betrag, sondern auch die PIN angeben: Nur wenn die PIN mit der des Kontos übereinstimmt,
# kann auch Geld abgebucht werden, ansonsten kommt es zu einer Fehlermeldung!

class Account():
    """
    Diese Klasse modelliert ein Bankkonto mit PIN-Schutz für Abhebungen.
    """
    def __init__(self, start, pin):
        """
        Der Konstruktor der Klasse `Account`.
        Initialisiert ein neues Konto mit Startguthaben und einer PIN.

        Args:
            start (float oder int): Das initiale Guthaben auf dem Konto.
            pin (int): Die vierstellige PIN für das Konto.
        """
        # Der Konstruktor empfängt das Startguthaben und die PIN und speichert sie als Instanzvariablen.
        self.credits = start
        self.pin = pin

    def display(self):
        """
        Gibt den aktuellen Kontostand des Kontos aus.
        """
        print(self.credits)

    def pay_in(self, money):
        """
        Zahlt einen bestimmten Betrag auf das Konto ein.

        Args:
            money (float oder int): Der Betrag, der eingezahlt werden soll.
        """
        # Die Methode zum Einzahlen addiert den einzuzahlenden Betrag zum Kontostand hinzu.
        self.credits += money

    def withdraw(self, money, pin):
        """
        Hebt einen bestimmten Betrag vom Konto ab, nach erfolgreicher PIN-Validierung.
        Verhindert Überziehungen und informiert bei falscher PIN.

        Args:
            money (float oder int): Der Betrag, der abgehoben werden soll.
            pin (int): Die vom Benutzer eingegebene PIN zur Verifikation.
        """
        # Zuerst wird geprüft, ob die übergebene PIN mit der hinterlegten PIN identisch ist.
        if pin == self.pin:
            # Wenn die PIN korrekt ist, wird anschließend geprüft, ob das Guthaben ausreicht.
            if self.credits >= money:
                # Wenn ja, wird der abzuhebende Betrag vom Konto abgebucht.
                self.credits -= money
            else:  # Falls das Guthaben nicht ausreicht,
                # wird eine Fehlermeldung ausgegeben, die den maximal abhebbaren Betrag anzeigt.
                print("Du kannst nur noch " + str(self.credits) + "€ abheben!")
        else:  # Wenn die PIN falsch war,
            # wird eine entsprechende Fehlermeldung ausgegeben.
            print("Falsche PIN! Du bist verhaftet! Hände hoch!")


# --- Test der Account-Klasse (Teil 2: Mit PIN) ---
Kunde111 = Account(500, 1234)  # Eine Instanz wird angelegt mit Startguthaben 500 und PIN 1234.
Kunde111.display()  # Kontostand wird ausgegeben.
Kunde111.pay_in(40)  # Eine Einzahlung wird getätigt.
Kunde111.display()  # Der aktualisierte Kontostand wird ausgegeben.
Kunde111.withdraw(25, 1234)  # Abhebung von 25€ mit korrekter PIN.
Kunde111.display()  # Der aktualisierte Kontostand wird ausgegeben.
Kunde111.withdraw(600, 1234)  # Abhebeversuch von 600€ mit korrekter PIN, aber unzureichendem Guthaben.


# ------------------
# Aufgabe 4: Modelliere einen Zug (Teil 1: Anzeige der Station)
# Jetzt wirst du Zugobjekte bauen! Erstelle die Klasse `_Train_`,
# die mit den Eigenschaften `_route_` und `_position_` initialisiert wird!
# Bei `_route_` handelt es sich um eine Liste mit den Haltebahnhöfen des Zuges.
# `_position_` steht für den Index des Bahnhofs aus der Liste, an dem sich der Zug gerade befindet
# bzw. von dem er zuletzt abgefahren ist (wo genau sich der Zug auf der Strecke zwischen zwei Bahnhöfen
# befindet, interessiert uns hier nicht). Mit der Methode `show_station()` soll der Name dieses Bahnhofs ausgegeben werden.

class Train():
    """
    Diese Klasse modelliert einen Zug, der eine festgelegte Route entlangfährt.
    Sie kann die aktuelle Station anzeigen.
    """
    def __init__(self, route, start):
        """
        Der Konstruktor der Klasse `Train`.
        Initialisiert einen Zug mit seiner Route und der aktuellen Position.

        Args:
            route (list): Eine Liste von Strings, die die Namen der Bahnhöfe auf der Route darstellen.
            start (int): Der Index des Startbahnhofs in der `route`-Liste.
        """
        # Dem Konstruktor wird die Liste der Haltestellen ('route') und der Index der aktuellen Station ('start')
        # mitgegeben. Diese werden als Instanzvariablen gespeichert.
        self.route = route
        self.position = start

    def show_station(self):
        """
        Gibt den Namen des Bahnhofs aus, an dem sich der Zug aktuell befindet.
        """
        # Die Methode gibt den Namen des Bahnhofs aus, der sich am aktuellen Index
        # in der 'route'-Liste befindet.
        if 0 <= self.position < len(self.route): # Sicherstellen, dass der Index gültig ist
            print(self.route[self.position])
        else:
            print("Fehler: Ungültige Zugposition auf der Route.")


# --- Test der Train-Klasse (Teil 1) ---
orientexpress = Train(["Paris", "Budapest", "Bukarest", "Istanbul"], 0)
orientexpress.show_station()


# -----------------------

# Aufgabe 4: Modelliere einen Zug (Teil 2: Bewegung des Zuges)
# Bisher sitzt ein Zug der Klasse `_Train_` noch in seinem Startbahnhof fest.
# Ergänze nun zwei Methoden `move()` und `move_back()`, mit denen man einen Zug auf seiner Route
# zur nächsten bzw. zur vorherigen Station bewegen kann, sofern es diese Station auf der Route gibt.
# Der Zug darf seine Route nicht verlassen!

class Train():
    """
    Diese Klasse modelliert einen Zug mit der Fähigkeit, sich auf seiner Route vor- und zurückzubewegen.
    """
    def __init__(self, route, start):
        """
        Der Konstruktor der Klasse `Train`.
        Initialisiert einen Zug mit seiner Route und der aktuellen Position.

        Args:
            route (list): Eine Liste von Strings, die die Namen der Bahnhöfe auf der Route darstellen.
            start (int): Der Index des Startbahnhofs in der `route`-Liste.
        """
        self.route = route
        self.position = start

    def show_station(self):
        """
        Gibt den Namen des Bahnhofs aus, an dem sich der Zug aktuell befindet.
        """
        if 0 <= self.position < len(self.route):
            print(self.route[self.position])
        else:
            print("Fehler: Ungültige Zugposition auf der Route.")

    def move(self):
        """
        Bewegt den Zug zur nächsten Station auf der Route.
        Verhindert, dass der Zug über das Ende der Route hinausfährt.
        """
        # Prüft, ob der Zug nicht bereits am Ende der Route ist.
        # Der Index der letzten Station ist `len(self.route) - 1`.
        if self.position < len(self.route) - 1:
            self.position += 1 # Erhöht den Index, um zur nächsten Station zu gelangen.
        else:
            print("Endstation, alles aussteigen!")

    def move_back(self):
        """
        Bewegt den Zug zur vorherigen Station auf der Route.
        Verhindert, dass der Zug über den Anfang der Route hinausfährt.
        """
        # Prüft, ob der Zug nicht bereits am Anfang der Route ist (Position > 0).
        if self.position > 0:
            self.position -= 1 # Verringert den Index, um zur vorherigen Station zu gelangen.
        else:
            print("Endstation, alles aussteigen!")


# --- Test der Train-Klasse (Teil 2: Bewegung) ---
orientexpress = Train(["Paris", "Budapest", "Bukarest", "Istanbul"], 0)
orientexpress.show_station()
orientexpress.move()
orientexpress.show_station()
orientexpress.move()
orientexpress.show_station()
orientexpress.move()
orientexpress.show_station()
orientexpress.move() # Versuch, über das Ende hinaus zu fahren
orientexpress.move_back()
orientexpress.show_station()


# ------------

# Aufgabe 4: Modelliere einen Zug (Teil 3: Bahnhof umfahren)
# Die Route soll nachträglich bearbeitet werden können, indem man mit einer Methode `bypass_station()`
# einen anzugebenden Haltebahnhof von der Route entfernt.
# Der Zug soll dann sicherheitshalber an den Start der Route versetzt werden,
# sofern er sich nicht schon dort befindet. **Tipp:** Erinnere dich an die Methoden für Listen! :-)

class Train():
    """
    Diese Klasse modelliert einen Zug und erweitert die Funktionalität um das Umfahren von Stationen.
    """
    def __init__(self, route, start):
        """
        Der Konstruktor der Klasse `Train`.
        Initialisiert einen Zug mit seiner Route und der aktuellen Position.

        Args:
            route (list): Eine Liste von Strings, die die Namen der Bahnhöfe auf der Route darstellen.
            start (int): Der Index des Startbahnhofs in der `route`-Liste.
        """
        self.route = route
        self.position = start

    def show_station(self):
        """
        Gibt den Namen des Bahnhofs aus, an dem sich der Zug aktuell befindet.
        """
        if 0 <= self.position < len(self.route):
            print(self.route[self.position])
        else:
            print("Fehler: Ungültige Zugposition auf der Route.")

    def move(self):
        """
        Bewegt den Zug zur nächsten Station auf der Route.
        Verhindert, dass der Zug über das Ende der Route hinausfährt.
        """
        if self.position < len(self.route) - 1:
            self.position += 1
        else:
            print("Endstation, alles aussteigen!")

    def move_back(self):
        """
        Bewegt den Zug zur vorherigen Station auf der Route.
        Verhindert, dass der Zug über den Anfang der Route hinausfährt.
        """
        if self.position > 0:
            self.position -= 1
        else:
            print("Endstation, alles aussteigen!")

    def bypass_station(self, station):
        """
        Entfernt einen bestimmten Bahnhof von der Route des Zuges.
        Setzt die Zugposition nach dem Entfernen sicherheitshalber auf den Start der Route zurück.

        Args:
            station (str): Der Name des Bahnhofs, der von der Route entfernt werden soll.
        """
        # Prüft, ob die angegebene Station in der Route existiert.
        if station in self.route:
            # Entfernt die Station aus der Route-Liste.
            self.route.remove(station)
            print(f"Station '{station}' von der Route entfernt.")
            # Setzt die Zugposition sicherheitshalber auf den Start der Route (Index 0) zurück.
            self.position = 0
            print("Der Zug wurde an den Start der Route zurückgesetzt.")
        else:
            print(f"Station '{station}' nicht auf der Route gefunden.")


# --- Test der Train-Klasse (Teil 3: Bahnhof umfahren) ---
orientexpress = Train(["Paris", "Budapest", "Bukarest", "Istanbul"], 0)
orientexpress.bypass_station("Budapest")
orientexpress.move()
orientexpress.show_station()