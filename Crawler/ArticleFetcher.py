import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .CrawledArticle import CrawledArticle # Import der CrawledArticle-Klasse aus demselben Package

class ArticleFetcher():
    """
    Diese Klasse ist für das Abrufen und Parsen von Artikeln von einer spezifischen Webseite zuständig.
    Sie navigiert auch über mehrere Seiten hinweg (Paginierung), um alle verfügbaren Artikel zu erfassen.
    Die Methode 'fetch' arbeitet als Generator, um Artikel effizient zu streamen.
    """
    def fetch(self):
        """
        Ruft Artikel von der vordefinierten Start-URL ab und navigiert durch alle paginierten Seiten.
        Diese Methode arbeitet als Generator und liefert CrawledArticle-Objekte sukzessive.

        Yields:
            CrawledArticle: Ein Objekt, das einen vollständig geparsten Artikel repräsentiert.
        """
        url = "http://python.beispiel.programmierenlernen.io/index.php"  # **Start-URL für den Web-Crawler.**
                                                                        # Dies ist die Einstiegsseite, von der aus
                                                                        # die Artikel gesammelt werden.

        # **Die 'fetch'-Methode wird als Generator implementiert.**
        # Anstatt alle gefundenen Artikel in einer Liste zu sammeln und am Ende zurückzugeben,
        # verwendet diese Methode 'yield'. Dies macht sie zu einem Generator, der Artikel
        # einzeln zurückgibt, sobald sie geparst wurden.
        # Vorteil: extrem speichereffizient, besonders bei der Verarbeitung großer Mengen
        # von Artikeln, da nicht alle Artikel gleichzeitig im Speicher gehalten werden müssen.

        # **Schleife für die Paginierung:**
        # Die 'while'-Schleife steuert die Navigation durch die Seiten.
        # Sie wird so lange ausgeführt, wie 'url' eine gültige URL für die nächste Seite enthält.
        # Die Schleife endet, sobald kein "Nächste Seite"-Button mehr gefunden wird und 'url'
        # auf einen leeren String ("") gesetzt wird.
        while url != "":
            print(f"Besuche URL: {url}")  # Zur **Debugging-Zwecken**: Zeigt die aktuell besuchte URL in der Konsole an.
                                        # Nützlich, um den Fortschritt des Crawlers zu verfolgen.
            time.sleep(1)  # **Kurze Pause von 1 Sekunde:** Dies ist eine kritische Maßnahme,
                           # um den Webserver nicht zu überlasten und das Risiko zu minimieren,
                           # dass die IP-Adresse des Crawlers blockiert wird (als Schutz vor DoS-Angriffen).

            try: # **Fehlerbehandlung für Netzwerk-Anfragen:**
                r = requests.get(url, timeout=10) # Sendet eine HTTP GET-Anfrage an die aktuelle URL, um den HTML-Inhalt abzurufen.
                                                  # Ein 'timeout' von 10 Sekunden verhindert, dass die Anfrage unendlich hängt.
                r.raise_for_status() # Löst einen HTTPError für schlechte Antworten (4xx oder 5xx) aus.
            except requests.exceptions.RequestException as e:
                print(f"Fehler beim Abrufen der URL {url}: {e}")
                url = "" # Setzt die URL auf leer, um die Schleife zu beenden und weitere Fehler zu vermeiden.
                continue # Springt zum nächsten Schleifendurchlauf oder beendet, falls url=""

            # Parsen des HTML-Inhalts der Antwort mit **BeautifulSoup**.
            # "html.parser" ist der eingebaute HTML-Parser von Python.
            # BeautifulSoup ermöglicht eine einfache Navigation und Extraktion von Daten aus dem HTML-Baum.
            doc = BeautifulSoup(r.text, "html.parser")

            # Iteriert über jedes HTML-Element, das die CSS-Klasse "card" besitzt, auf der aktuellen Seite.
            # Jede "card" wird als visueller Container für einen einzelnen Artikel auf der Webseite interpretiert.
            for card in doc.select(".card"):
                # Extrahiert das Emoji aus dem Element mit der Klasse "emoji" innerhalb der aktuellen 'card'.
                emoji = card.select_one(".emoji").text.strip() # .strip() entfernt führende/nachfolgende Leerzeichen.
                # Extrahiert den Haupttext des Artikels aus dem Element mit der Klasse "card-text".
                content = card.select_one(".card-text").text.strip()
                # Sucht das zweite <span>-Element innerhalb eines Elements mit der Klasse "card-title"
                # und extrahiert dessen Text als Titel. (Annahme: Das erste <span> könnte z.B. eine Nummer sein).
                title = card.select(".card-title span")[1].text.strip()
                # Extrahiert die relative Bild-URL aus dem 'src'-Attribut des <img>-Tags innerhalb der 'card'.
                # Anschließend wird sie mit urljoin in eine vollständige, absolute URL umgewandelt.
                # Dies ist wichtig, da 'src'-Attribute oft relative Pfade enthalten.
                image = urljoin(url, card.select_one("img").attrs["src"])

                # **Der 'yield'-Befehl:**
                # Gibt ein neu erstelltes CrawledArticle-Objekt zurück, ohne die Funktion zu beenden.
                # Die Ausführung der Funktion wird bis zum nächsten Aufruf von 'next()' (im Fall eines Generators)
                # oder zur nächsten Iteration der Schleife pausiert.
                yield CrawledArticle(title, emoji, content, image)

            # **Paginierungslogik: Suche nach dem "Zur nächsten Seite"-Button**
            # Sucht nach dem HTML-Element, das den "Zur nächsten Seite"-Button repräsentiert.
            # Dieser wird typischerweise innerhalb eines Containers mit der Klasse ".navigation" gefunden
            # und selbst mit der Klasse ".btn" identifiziert.
            next_button = doc.select_one(".navigation .btn")

            # Überprüft, ob ein "Nächste Seite"-Button auf der aktuellen Seite gefunden wurde.
            if next_button:
                # Wenn ja, wird der Wert des 'href'-Attributs abgerufen, der die URL der nächsten Seite enthält.
                next_href = next_button.attrs["href"]
                # Der relative 'href'-Pfad wird in eine absolute URL umgewandelt,
                # indem die aktuelle 'url' als Basis verwendet wird.
                next_href = urljoin(url, next_href)
                # Die 'url' für den nächsten Schleifendurchlauf wird auf die neu gefundene URL der nächsten Seite gesetzt.
                url = next_href
            else:
                # Wenn kein "Nächste Seite"-Button gefunden wurde (d.h., der Crawler hat die letzte Seite erreicht),
                # wird 'url' auf einen leeren String ("") gesetzt.
                # Dies bewirkt, dass die 'while'-Schleife beim nächsten Prüfen der Bedingung (url != "") beendet wird.
                url = ""

        # **Kein explizites 'return articles' hier erforderlich:**
        # Da 'fetch' als Generator implementiert ist und Artikel sukzessive über 'yield' zurückgibt,
        # ist kein explizites 'return'-Statement am Ende der Funktion nötig.
        # Der Generator beendet seine Ausführung automatisch, sobald die Schleife abgeschlossen ist
        # und keine weiteren 'yield'-Statements erreicht werden können.

