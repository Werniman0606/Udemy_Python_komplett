"""
Statt einer Liste, fügen wir nun einen Generator ein, indem wir die Listengenerierung (articles = []) entfernen und
auch den gecrawlten Inhalt (CrawledArticle) nicht mehr per append an die Liste anhängen,sondern die Funktion per
Yield-Befehl stoppen

"""

import requests  # Importiert das 'requests'-Modul, um HTTP-Anfragen (z.B. Webseiten abrufen) durchzuführen.
from bs4 import BeautifulSoup  # Importiert 'BeautifulSoup' aus dem 'bs4'-Modul, um HTML- und XML-Dokumente zu parsen.
from urllib.parse import \
    urljoin  # Importiert 'urljoin' für das Zusammenfügen von Basis-URLs und relativen Pfaden zu absoluten URLs.
import time  # Importiert das 'time'-Modul, um Zeitverzögerungen zu steuern (gut, um Server nicht zu überlasten).


# %%
class CrawledArticle():
    # Diese Klasse dient als einfacher Datencontainer für die Informationen eines jeden Artikels.
    def __init__(self, title, emoji, content, image):
        self.title = title  # Der Titel des Artikels.
        self.emoji = emoji  # Das Emoji, das den Artikel begleitet.
        self.content = content  # Der Textinhalt des Artikels.
        self.image = image  # Die absolute URL des Artikelbildes.

    def __repr__(self):
        # Diese spezielle Methode definiert, wie ein CrawledArticle-Objekt ausgegeben wird,
        # wenn es direkt gedruckt oder in einer Liste angezeigt wird.
        return f"CrawledArticle(Titel: '{self.title}', Emoji: '{self.emoji}')"


class ArticleFetcher():
    # Diese Klasse ist für das Abrufen und Parsen der Artikel von der Webseite zuständig,
    # einschließlich der Navigation über mehrere Seiten hinweg.
    def fetch(self):
        url = "http://python.beispiel.programmierenlernen.io/index.php"  # **Start-URL für den Crawler.**

        # **Wichtige Änderung: Die Methode wird zu einem Generator**
        # Statt eine Liste aller Artikel zu erstellen und am Ende zurückzugeben,
        # verwenden wir 'yield'. Das macht 'fetch' zu einem Generator.
        # Ein Generator gibt die Artikel einzeln zurück, sobald sie gefunden werden,
        # was bei großen Datenmengen sehr speichereffizient ist.

        # **Schleife für die Paginierung:**
        # Die 'while'-Schleife läuft so lange, wie 'url' einen gültigen Wert hat.
        # Sie stoppt, wenn keine "Nächste Seite"-Schaltfläche mehr gefunden wird und 'url' auf "" gesetzt wird.
        while url != "":
            print(f"Besuche URL: {url}")  # Zur Debugging-Zwecken: Zeigt die aktuell besuchte URL an.
            time.sleep(1)  # **Kurze Pause von 1 Sekunde:** Wichtig, um den Server nicht zu überlasten
            # und das Risiko einer Blockierung zu minimieren.

            r = requests.get(url)  # Sendet eine HTTP GET-Anfrage an die aktuelle URL, um den HTML-Inhalt zu holen.
            doc = BeautifulSoup(r.text, "html.parser")  # Parsen des HTML-Inhalts der Antwort mit BeautifulSoup
            # für eine einfache Navigation und Datenextraktion.

            # Iteriert über jedes HTML-Element mit der CSS-Klasse "card" auf der aktuellen Seite.
            # Jede "card" repräsentiert einen einzelnen Artikel auf der Webseite.
            for card in doc.select(".card"):
                emoji = card.select_one(".emoji").text  # Extrahiert das Emoji aus dem Element mit der Klasse "emoji".
                content = card.select_one(".card-text").text  # Extrahiert den Haupttext des Artikels.
                # Sucht das zweite <span>-Element innerhalb eines Elements mit der Klasse "card-title"
                # und extrahiert dessen Text als Titel.
                title = card.select(".card-title span")[1].text
                # Extrahiert die relative Bild-URL aus dem 'src'-Attribut des <img>-Tags
                # und wandelt sie dann mit urljoin in eine vollständige, absolute URL um.
                image = urljoin(url, card.select_one("img").attrs["src"])

                # **Der 'yield'-Befehl:**
                # Gibt ein CrawledArticle-Objekt zurück, ohne die Funktion zu beenden.
                # Die Ausführung der Funktion wird bis zum nächsten 'next()' oder zur nächsten Iteration pausiert.
                yield CrawledArticle(title, emoji, content, image)

            # **Paginierungslogik: Suche nach dem "Zur nächsten Seite"-Button**
            # Sucht nach dem HTML-Element, das den "Zur nächsten Seite"-Button darstellt.
            # Dieser wird typischerweise innerhalb eines Bereichs mit der Klasse ".navigation"
            # und selbst mit der Klasse ".btn" identifiziert.
            next_button = doc.select_one(".navigation .btn")

            # Überprüft, ob ein "Nächste Seite"-Button auf der aktuellen Seite gefunden wurde.
            if next_button:
                # Wenn ja, hole den Wert des 'href'-Attributs, der die URL der nächsten Seite enthält.
                next_href = next_button.attrs["href"]
                # Wandelt den relativen 'href'-Pfad in eine absolute URL um,
                # indem die aktuelle 'url' als Basis für die Verknüpfung verwendet wird.
                next_href = urljoin(url, next_href)
                # Setzt die 'url' für den nächsten Schleifendurchlauf auf die neu gefundene URL der nächsten Seite.
                url = next_href
            else:
                # Wenn kein "Nächste Seite"-Button gefunden wurde (d.h., wir sind auf der letzten Seite),
                # wird 'url' auf einen leeren String ("") gesetzt. Dies beendet die 'while'-Schleife
                # beim nächsten Prüfen der Schleifenbedingung (url != "").
                url = ""

        # **Kein 'return articles' hier:**
        # Da 'fetch' ein Generator ist und die Artikel über 'yield' zurückgibt,
        # ist kein explizites 'return' Statement am Ende der Funktion nötig.
        # Der Generator beendet seine Ausführung automatisch, wenn die Schleife abgeschlossen ist.


# --- Ausführung des Crawlers ---
fetcher = ArticleFetcher()  # Erstellt eine Instanz der ArticleFetcher-Klasse.
# **Aufruf des Generators:**
# 'fetcher.fetch()' gibt nun ein Generator-Objekt zurück, das Artikel liefert,
# sobald sie vom Crawler gefunden werden. 'all_articles' ist dieses Generator-Objekt.
all_articles = fetcher.fetch()

# --- Ausgabe der Ergebnisse ---
print("\n--- Alle gesammelten Artikel ---")
# **Iteration über den Generator:**
# Die 'for'-Schleife iteriert über das Generator-Objekt 'all_articles'.
# Bei jedem Schleifendurchlauf wird der nächste verfügbare Artikel vom Generator angefordert,
# bis der Generator keine weiteren Artikel mehr liefert (d.h., alle Seiten wurden durchsucht).
for article in all_articles:
    print(f"{article.emoji}: {article.title}")

"""Ausgabe:
Besuche URL: http://python.beispiel.programmierenlernen.io/index.php
😩: Polarised modular conglomeration
😐: Cross-group contextually-based middleware
😌: De-engineered encompassing structure
😚: Fully-configurable multi-tasking interface
😠: Versatile eco-centric core
😮: Optional maximized utilisation
😢: Open-architected secondary product
Besuche URL: http://python.beispiel.programmierenlernen.io/index.php?page=2
😠: Realigned zerotolerance function
😆: Quality-focused user-facing help-desk
😤: Proactive user-facing opensystem
😟: Decentralized holistic moderator
😌: Mandatory tangible application
😓: Digitized dedicated budgetarymanagement
😞: Organized well-modulated concept
usw.
"""



"""
Absolut! Gerne beschreibe ich die Reihenfolge des Codes und was wann passiert, Schritt für Schritt.
Ablauf des Web-Crawlers: Schritt für Schritt erklärt

Dein Code ist darauf ausgelegt, Artikel von einer Webseite zu sammeln, die über mehrere Seiten hinweg paginiert ist. Hier ist die genaue Reihenfolge, wie der Code ausgeführt wird:
1. Vorbereitung und Definitionen (Start des Skripts)

    Importe: Zuerst werden die benötigten Bibliotheken geladen:
        requests für das Senden von HTTP-Anfragen (Webseiten herunterladen).
        BeautifulSoup zum Parsen des HTML-Inhalts und Extrahieren von Daten.
        urljoin zum Zusammenfügen von Basis-URLs und relativen Pfaden.
        time für das Einfügen von Pausen.
    Klassen-Definitionen:
        Die Klasse CrawledArticle wird als Bauplan für jedes Artikelobjekt definiert. Sie legt fest, welche Informationen (Titel, Emoji, Inhalt, Bild-URL) ein gescrappter Artikel haben wird und wie er später lesbar ausgegeben wird (__repr__-Methode).
        Die Klasse ArticleFetcher wird definiert. Sie enthält die gesamte Logik für das Crawling – also das Navigieren zwischen den Seiten und das Extrahieren der Daten.

2. Initialisierung des Crawling-Prozesses (Am Ende des Skripts)

    Instanziierung: Ganz am Ende deines Skripts, außerhalb der Klassen, wird eine Instanz (ein Objekt) der ArticleFetcher-Klasse erstellt: fetcher = ArticleFetcher(). Dein Crawler ist nun bereit.
    Aufruf der fetch-Methode: Die fetch()-Methode dieses fetcher-Objekts wird aufgerufen: all_articles = fetcher.fetch(). Hier beginnt die eigentliche Arbeit des Crawlers.

3. Start der Paginierungs-Schleife (Innerhalb der fetch()-Methode)

    Start-URL: Im Inneren der fetch()-Methode wird die Variable url mit der initialen URL der Webseite belegt (der ersten Seite).
    Die while-Schleife: Eine while-Schleife beginnt: while url != "". Diese Schleife ist das Herzstück der Paginierungslogik. Sie wird so lange ausgeführt, wie die url-Variable einen Wert hat (also eine Seite zum Besuchen existiert). Sobald keine nächste Seite mehr gefunden wird und url auf einen leeren String gesetzt wird, endet die Schleife.

4. Verarbeitung einer einzelnen Seite (Pro Durchlauf der while-Schleife)

    Statusmeldung & Pause: Bei jedem Schleifendurchlauf wird die aktuell besuchte URL ausgegeben (print(f"Besuche URL: {url}")). Direkt danach wird eine Pause von 1 Sekunde (time.sleep(1)) eingelegt. Das ist entscheidend, um den Webserver nicht zu überlasten und einer möglichen Blockierung vorzubeugen.
    Webseiten-Anfrage: requests.get(url) sendet eine HTTP-GET-Anfrage an die aktuelle URL, um den vollständigen HTML-Inhalt der Seite herunterzuladen.
    HTML Parsen: Der heruntergeladene HTML-Text (r.text) wird an BeautifulSoup übergeben (doc = BeautifulSoup(r.text, "html.parser")). Dadurch wird der HTML-Text in ein Python-Objekt umgewandelt, das leicht durchsucht und manipuliert werden kann.

5. Extrahieren der Artikel auf der aktuellen Seite

    Artikel-Iteration: Eine for-Schleife (for card in doc.select(".card"):) durchläuft alle HTML-Elemente auf der aktuellen Seite, die die CSS-Klasse "card" besitzen. Jedes dieser Elemente wird als Container für einen Artikel betrachtet.
    Daten-Extraktion: Innerhalb dieser for-Schleife werden für jede "card" die spezifischen Informationen des Artikels extrahiert:
        Das Emoji (.emoji-Klasse).
        Der Inhalt (.card-text-Klasse).
        Der Titel (das zweite <span>-Element innerhalb von .card-title).
        Die Bild-URL: Hier wird der Wert des src-Attributs des <img>-Tags geholt. Ganz wichtig: urljoin(url, ...) kombiniert diese oft relative Bild-URL mit der aktuellen Basis-URL der Seite, um eine vollständige, absolute URL zu erzeugen, die später direkt aufrufbar ist.
    Artikel "Yielding": Statt die gesammelten Daten in eine Liste einzufügen, wird yield CrawledArticle(...) verwendet. Das bedeutet, dass ein CrawledArticle-Objekt sofort zurückgegeben wird, ohne die fetch-Methode zu verlassen. Die Methode pausiert und wartet auf den nächsten Abruf.

6. Paginierungslogik: Suche nach der nächsten Seite

    "Nächste Seite"-Button suchen: Nachdem alle Artikel der aktuellen Seite über yield bereitgestellt wurden, sucht der Code nach dem HTML-Element, das den "Zur nächsten Seite"-Button repräsentiert (next_button = doc.select_one(".navigation .btn")).
    Bedingte Logik (if/else):
        Wenn der Button gefunden wird (if next_button ist True):
            Der Wert des href-Attributs (der Link zur nächsten Seite) wird aus dem Button-Element ausgelesen (next_href = next_button.attrs["href"]).
            Auch dieser relative Pfad wird mit urljoin(url, next_href) in eine absolute URL umgewandelt.
            Die url-Variable wird auf diese neu gefundene URL der nächsten Seite gesetzt (url = next_href). Dies sorgt dafür, dass die while-Schleife im nächsten Durchlauf diese neue Seite lädt und verarbeitet.
        Wenn der Button NICHT gefunden wird (else-Zweig):
            Das bedeutet, der Crawler hat die letzte Seite erreicht.
            Die url-Variable wird auf einen leeren String (url = "") gesetzt. Dadurch wird die Bedingung der while-Schleife (url != "") beim nächsten Prüfen False, und die Schleife beendet sich.

7. Abschluss und Ergebnisausgabe

    Generator-Ende: Sobald die while-Schleife in der fetch()-Methode beendet ist (weil url ein leerer String ist), signalisiert der Generator, dass keine weiteren Werte mehr geliefert werden. Die fetch()-Methode wird ohne ein explizites return beendet.
    Iteration über den Generator: Außerhalb der Klasse, im Hauptteil des Skripts, wo all_articles = fetcher.fetch() aufgerufen wurde, wird nun über das zurückgegebene Generator-Objekt iteriert: for article in all_articles:.
    Ausgabe: Bei jedem Durchlauf dieser for-Schleife wird der nächste verfügbare Artikel vom Generator angefordert und dessen Emoji und Titel auf der Konsole ausgegeben. Dies geschieht, bis der Generator keine Artikel mehr liefert.

Dieser schrittweise Ablauf ermöglicht es deinem Crawler, systematisch alle Seiten der Webseite zu besuchen, die relevanten Daten zu extrahieren und sie dir effizient zur Verfügung zu stellen.
------------------------

Änderungen von der Listen-basierten zur Generator-basierten Version

Die Kernänderungen, um von einer Listen-basierten Datensammlung zu einem Generator zu wechseln und die Paginierung zu implementieren, betreffen hauptsächlich die fetch-Methode in der ArticleFetcher-Klasse.

Hier sind die spezifischen Zeilen, die entweder entfernt oder geändert wurden:
1. Initialisierung der Artikelliste (Entfernt)

In der alten Version wurde eine leere Liste namens articles initialisiert, um alle gesammelten CrawledArticle-Objekte aufzunehmen:
Python

# --- DIESE ZEILE WURDE ENTFERNT ---
articles = []  # Initialisiert eine leere Liste, in der alle extrahierten 'CrawledArticle'-Objekte gespeichert werden.

Grund für die Entfernung: Mit einem Generator brauchen wir diese Liste nicht mehr. Der Generator "gibt" die Artikel einzeln zurück, sobald sie gefunden werden, ohne sie alle im Speicher sammeln zu müssen.
2. Hinzufügen zur Artikelliste (Geändert zu yield)

Anstatt die gesammelten Artikel der articles-Liste hinzuzufügen, wurde der Aufruf an CrawledArticle so geändert, dass er jetzt mit dem Schlüsselwort yield verwendet wird.

Alte Zeile:
Python

# --- DIESE ZEILE WURDE GEÄNDERT ---
# crawled = CrawledArticle(title, emoji, content, image)  # Erstellt ein neues 'CrawledArticle'-Objekt mit den extrahierten und bereinigten Daten.
# articles.append(crawled)  # Fügt das neu erstellte Artikel-Objekt der 'articles'-Liste hinzu.

Neue Zeile:
Python

# --- GEÄNDERT ZU DIESER ZEILE ---
yield CrawledArticle(title, emoji, content, image)  # Gibt das Artikel-Objekt als Teil des Generators zurück.

Grund für die Änderung: yield macht die fetch-Methode zu einem Generator. Es gibt das erzeugte Objekt zurück und pausiert die Funktion, anstatt sie zu beenden. Beim nächsten Aufruf wird die Ausführung an der Stelle fortgesetzt, wo sie aufgehört hat.
3. Rückgabe der Artikelliste (Entfernt)

In der alten Version wurde am Ende der fetch-Methode die gesammelte Liste aller Artikel zurückgegeben:
Python

# --- DIESE ZEILE WURDE ENTFERNT ---
# return articles  # Gibt die Liste aller gescrapten Artikel-Objekte zurück.

Grund für die Entfernung: Da die fetch-Methode jetzt ein Generator ist, gibt sie keine explizite Liste mehr zurück. Die Artikel werden einzeln über yield geliefert. Ein Generator beendet seine Ausführung implizit, wenn er keine weiteren yield-Anweisungen mehr erreicht (in deinem Fall, wenn die while-Schleife endet). Das Beibehalten dieser Zeile war auch die Ursache für den NameError, den du zuvor hattest.

Zusätzlich zu diesen Änderungen wurde die while-Schleife für die Paginierung und die time.sleep(1)-Pause hinzugefügt, um die Funktionalität des Multi-Seiten-Crawlings zu ermöglichen, die in der ursprünglichen Version nicht vorhanden war.

Diese Anpassungen machen deinen Crawler nicht nur fähig, mehrere Seiten zu durchsuchen, sondern auch deutlich speichereffizienter durch die Nutzung des Generator-Prinzips.


"""
