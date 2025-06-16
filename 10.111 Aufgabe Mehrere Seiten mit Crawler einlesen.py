"""
## Aufgabe: Crawler

**Aufgabe:**


- Passe den ArticleFetcher so an, dass er die Informationen aus allen Seiten extrahiert

Hier nochmal die URL: http://python.beispiel.programmierenlernen.io/index.php

**Tipps:**

- Schau dir zuerst an, wie du den Button "Zur nächsten Seite" ansteuern kannst.

- Wie greifst du von Python aus auf das "href" - Attribut dieses Buttons zu?

- (Optional): Probier ggf. zuerst, nur die Infos der ersten 2 Seiten zu holen. Kannst du darauf aufbauend das Programm verallgemeinern, so dass es alle Seiten einliest?

- Du kannst dich daran orientieren, ob es einen "Zur nächsten Seite"-Button gibt, oder nicht. Wenn es diesen Button nicht mehr gibt, bist du auf der letzten Seite angelangt. Welcher Schleifentyp bietet sich hier an, wenn du die Schleife erst dann stoppen willst, wenn es den Button nicht mehr gibt?
"""

import requests  # Importiert das 'requests'-Modul, um HTTP-Anfragen (z.B. Webseiten abrufen) durchzuführen.
from bs4 import BeautifulSoup  # Importiert 'BeautifulSoup' aus dem 'bs4'-Modul, um HTML- und XML-Dokumente zu parsen.
from urllib.parse import urljoin  # Importiert 'urljoin' für das Zusammenfügen von Basis-URLs und relativen Pfaden zu absoluten URLs.
import time  # Importiert das 'time'-Modul, um Zeitverzögerungen zu steuern (gut, um Server nicht zu überlasten).


# %%
class CrawledArticle():
    # Diese Klasse dient als einfacher Datencontainer für die Informationen eines jeden Artikels.
    def __init__(self, title, emoji, content, image):
        self.title = title    # Der Titel des Artikels.
        self.emoji = emoji    # Das Emoji, das den Artikel begleitet.
        self.content = content  # Der Textinhalt des Artikels.
        self.image = image    # Die absolute URL des Artikelbildes.

    def __repr__(self):
        # Diese spezielle Methode definiert, wie ein CrawledArticle-Objekt ausgegeben wird,
        # wenn es direkt gedruckt oder in einer Liste angezeigt wird.
        return f"CrawledArticle(Titel: '{self.title}', Emoji: '{self.emoji}')"


class ArticleFetcher():
    # Diese Klasse ist für das Abrufen und Parsen der Artikel von der Webseite zuständig,
    # einschließlich der Navigation über mehrere Seiten hinweg.
    def fetch(self):
        url = "http://python.beispiel.programmierenlernen.io/index.php"  # Start-URL für den Crawler.
        articles = []  # Eine leere Liste, um alle gesammelten Artikel über alle Seiten hinweg zu speichern.

        # Eine Schleife, die so lange läuft, wie 'url' einen gültigen Wert hat.
        # Sie stoppt, wenn keine "Nächste Seite"-Schaltfläche mehr gefunden wird und 'url' auf "" gesetzt wird.
        while url != "":
            print(f"Besuche URL: {url}")  # Zur Debugging-Zwecken: Zeigt die aktuell besuchte URL an.
            time.sleep(1)  # Kurze Pause von 1 Sekunde, um den Server nicht zu überlasten (gute Praxis beim Web-Scraping).

            r = requests.get(url)  # Sendet eine HTTP GET-Anfrage an die aktuelle URL.
            doc = BeautifulSoup(r.text, "html.parser")  # Parsen des HTML-Inhalts der Antwort mit BeautifulSoup.

            # Iteriert über jedes HTML-Element mit der CSS-Klasse "card" auf der aktuellen Seite.
            # Jede "card" repräsentiert einen einzelnen Artikel.
            for card in doc.select(".card"):
                emoji = card.select_one(".emoji").text  # Extrahiert das Emoji.
                content = card.select_one(".card-text").text  # Extrahiert den Artikeltext.
                title = card.select(".card-title span")[1].text  # Extrahiert den Titel des Artikels.
                # Extrahiert die Bild-URL und wandelt sie mit urljoin in eine absolute URL um.
                image = urljoin(url, card.select_one("img").attrs["src"])

                # Erstellt ein CrawledArticle-Objekt mit den gesammelten Daten.
                crawled = CrawledArticle(title, emoji, content, image)
                articles.append(crawled)  # Fügt das Objekt zur Gesamtliste der Artikel hinzu.

            # Sucht nach dem "Zur nächsten Seite"-Button.
            # Der Button hat die Klasse "btn" und befindet sich typischerweise im ".navigation"-Bereich.
            next_button = doc.select_one(".navigation .btn")

            # Überprüft, ob ein "Nächste Seite"-Button gefunden wurde.
            if next_button:
                # Wenn ja, hole den Wert des 'href'-Attributs (die URL der nächsten Seite).
                next_href = next_button.attrs["href"]
                # Wandelt den relativen 'href'-Pfad in eine absolute URL um.
                next_href = urljoin(url, next_href)
                url = next_href  # Setzt die 'url' für den nächsten Schleifendurchlauf auf die URL der nächsten Seite.
            else:
                # Wenn kein "Nächste Seite"-Button gefunden wurde (d.h., wir sind auf der letzten Seite),
                # wird 'url' auf einen leeren String gesetzt, um die while-Schleife zu beenden.
                url = ""

        return articles  # Gibt die vollständige Liste aller gesammelten Artikel von allen Seiten zurück.


# --- Ausführung des Crawlers ---
fetcher = ArticleFetcher()  # Erstellt eine Instanz der ArticleFetcher-Klasse.
# Ruft die fetch()-Methode auf, die alle Artikel von allen Seiten sammelt.
# Die gesammelten Artikel werden in 'all_articles' gespeichert.
all_articles = fetcher.fetch()

# --- Ausgabe der Ergebnisse ---
print("\n--- Alle gesammelten Artikel ---")
# Iteriert durch die Liste aller gesammelten Artikel und gibt Titel und Emoji für jeden Artikel aus.
for article in all_articles:
    print(f"{article.emoji}: {article.title}")


"""
Reihenfolge des Ablaufs (Was passiert wann?)

    Vorbereitung (Imports und Klassen-Definitionen):
        Die benötigten Bibliotheken (requests, BeautifulSoup, urljoin, time) werden importiert.
        Die Klasse CrawledArticle wird definiert. Sie ist ein Bauplan dafür, wie die Daten eines einzelnen Artikels gespeichert werden. Ihre __repr__ Methode sorgt dafür, dass die Objekte später lesbar ausgegeben werden.
        Die Klasse ArticleFetcher wird definiert. Sie enthält die Logik zum Navigieren und Extrahieren der Daten.

    Initialisierung des Crawling-Prozesses:
        Ganz am Ende des Skripts wird eine Instanz von ArticleFetcher erstellt: fetcher = ArticleFetcher().
        Die fetch()-Methode dieser Instanz wird aufgerufen: all_articles = fetcher.fetch(). Hier beginnt die eigentliche Arbeit.

    Start der Paginierungs-Schleife (in fetch()):
        Innerhalb der fetch()-Methode wird die url auf die Startseite gesetzt ("http://python.beispiel.programmierenlernen.io/index.php").
        Eine leere Liste articles wird erstellt, die alle Artikel von allen Seiten sammeln wird.
        Eine while-Schleife beginnt. Diese Schleife wird so lange laufen, wie die url nicht leer ist. Das ist unser Mechanismus, um Seite für Seite zu besuchen.

    Verarbeitung einer einzelnen Seite (innerhalb der while-Schleife):
        URL-Anzeige und Pause: Die aktuelle url wird zur Information ausgegeben, und das Skript wartet kurz (time.sleep(1)) um den Server nicht zu überlasten.
        Anfrage senden: requests.get(url) lädt den HTML-Inhalt der aktuellen Seite herunter.
        HTML parsen: BeautifulSoup(r.text, "html.parser") wandelt den heruntergeladenen HTML-Text in ein durchsuchbares Objekt um.

    Extrahieren der Artikel auf der aktuellen Seite:
        Eine for-Schleife durchläuft alle HTML-Elemente, die die CSS-Klasse "card" haben. Jede dieser "Cards" repräsentiert einen Artikel.
        Für jede "Card" werden die spezifischen Informationen (Emoji, Inhalt, Titel, Bild-URL) mit select_one() und attrs["src"] extrahiert.
        Wichtig: Die Bild-URL wird mit urljoin(url, ...) von einem relativen Pfad (z.B. ./img/1.jpg) in eine absolute URL (z.B. https://.../img/1.jpg) umgewandelt.
        Ein CrawledArticle-Objekt wird mit diesen Daten erstellt und zur globalen articles-Liste hinzugefügt.

    Finden des "Nächste Seite"-Buttons (Paginierungslogik):
        Nachdem alle Artikel der aktuellen Seite verarbeitet wurden, sucht der Code nach einem Element, das den "Nächste Seite"-Button darstellt (.navigation .btn).
        Wenn der Button gefunden wird:
            Sein href-Attribut (die URL der nächsten Seite) wird ausgelesen.
            Diese URL wird ebenfalls mit urljoin in eine absolute URL umgewandelt.
            Die url-Variable wird auf diese neue URL gesetzt. Der while-Schleifenmechanismus erkennt dies und startet den nächsten Durchlauf mit der nächsten Seite.
        Wenn der Button NICHT gefunden wird:
            Das bedeutet, wir sind auf der letzten Seite angekommen.
            Die url-Variable wird auf einen leeren String ("") gesetzt. Dadurch wird die while-Schleife beim nächsten Prüfen der Bedingung (url != "") beendet.

    Abschluss und Rückgabe:
        Sobald die while-Schleife beendet ist (weil alle Seiten durchsucht wurden), gibt die fetch()-Methode die vollständige Liste articles zurück.

    Ergebnisausgabe:
        Außerhalb der Klassen wird die zurückgegebene Liste (all_articles) durchlaufen.
        Für jeden article in dieser Liste wird der Titel und das Emoji auf der Konsole ausgegeben, um die gesammelten Daten zu präsentieren.
"""