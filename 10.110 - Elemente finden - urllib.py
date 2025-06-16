# --- Problem: Relative URLs lösen ---
# In dieser Sektion geht es darum, ein häufiges Problem beim Web-Scraping zu lösen:
# Wenn wir Bilder oder andere Ressourcen von einer Webseite auslesen, erhalten wir oft
# nur einen "relativen Pfad" (z.B. './img/1.jpg') anstatt der vollständigen URL
# (z.B. 'https://python.beispiel.programmierenlernen.io/img/1.jpg').
# Diesen relativen Pfad können wir nicht direkt verwenden, um auf die Ressource zuzugreifen.
# Wir müssen ihn in eine absolute URL umwandeln. Dafür nutzen wir das 'urljoin'-Modul.

import requests  # Importiert das 'requests'-Modul, um HTTP-Anfragen (z.B. das Abrufen von Webseiten) durchzuführen.
from bs4 import BeautifulSoup  # Importiert 'BeautifulSoup' aus dem 'bs4'-Modul, um HTML- und XML-Dokumente zu parsen und Daten daraus zu extrahieren.
from urllib.parse import urljoin  # Importiert die 'urljoin'-Funktion aus dem 'urllib.parse'-Modul. Diese Funktion ist entscheidend, um relative URLs in absolute URLs umzuwandeln.


# %%
class CrawledArticle:  # Definiert eine Klasse namens 'CrawledArticle'.
    # Diese Klasse dient als Datencontainer, um die extrahierten Informationen eines Artikels strukturiert zu speichern.
    def __init__(self, title, emoji, content, image):
        # Der Konstruktor der Klasse. Er wird aufgerufen, wenn ein neues 'CrawledArticle'-Objekt erstellt wird.
        self.title = title    # Speichert den Titel des Artikels.
        self.emoji = emoji    # Speichert das Emoji des Artikels.
        self.content = content  # Speichert den Textinhalt des Artikels.
        self.image = image    # Speichert die (absolute) Bild-URL des Artikels.

    def __repr__(self):
        # Die __repr__-Methode definiert, wie ein Objekt dieser Klasse als String dargestellt wird,
        # z.B. wenn es in einer Liste ausgegeben wird. Das macht die Ausgabe lesbarer.
        return f"CrawledArticle(Titel: '{self.title}', Emoji: '{self.emoji}')"


class ArticleFetcher:  # Definiert eine Klasse namens 'ArticleFetcher'.
    # Diese Klasse ist dafür zuständig, die Artikel von der Webseite abzurufen und zu parsen.
    def fetch(self):  # Definiert die Methode 'fetch', die den eigentlichen Scraping-Prozess durchführt.
        url = "http://python.beispiel.programmierenlernen.io/index.php"  # Definiert die Basis-URL der zu scrapenden Webseite.
        r = requests.get(url)  # Sendet eine GET-Anfrage an die definierte URL und erhält die HTML-Antwort.
        doc = BeautifulSoup(r.text, "html.parser")  # Erstellt ein BeautifulSoup-Objekt aus dem HTML-Inhalt der Antwort.
                                                    # "html.parser" ist der Parser, der zum Analysieren des HTMLs verwendet wird.

        articles = []  # Initialisiert eine leere Liste, in der alle extrahierten 'CrawledArticle'-Objekte gespeichert werden.
        for card in doc.select(".card"):  # Iteriert über jedes HTML-Element mit der CSS-Klasse "card".
                                            # Jede "card" repräsentiert typischerweise einen Artikel auf der Webseite.
            emoji = card.select_one(".emoji").text  # Sucht das erste Element mit der Klasse "emoji" innerhalb der aktuellen "card" und extrahiert dessen Text (das Emoji-Zeichen).
            content = card.select_one(".card-text").text  # Sucht das erste Element mit der Klasse "card-text" und extrahiert dessen Text (den Artikelinhalt).
            title = card.select(".card-title span")[1].text  # Sucht alle 'span'-Elemente innerhalb eines Elements mit der Klasse "card-title"
                                                            # und extrahiert den Text des ZWEITEN 'span'-Elements (Index 1), welches den eigentlichen Titel enthält.

            # Extrahieren und Umwandeln der Bild-URL:
            # card.select_one("img").attrs["src"] holt den 'src'-Attributwert des <img>-Tags,
            # der oft ein relativer Pfad ist (z.B. './img/1.jpg').
            # urljoin(url, ...) kombiniert die Basis-URL (url) mit dem relativen Pfad,
            # um eine vollständige, absolute URL (z.B. 'https://python.beispiel.programmierenlernen.io/img/1.jpg') zu erstellen.
            image = urljoin(url, card.select_one("img").attrs["src"])

            crawled = CrawledArticle(title, emoji, content, image)  # Erstellt ein neues 'CrawledArticle'-Objekt mit den extrahierten und bereinigten Daten.
            articles.append(crawled)  # Fügt das neu erstellte Artikel-Objekt der 'articles'-Liste hinzu.
        return articles  # Gibt die Liste aller gescrapten Artikel-Objekte zurück.


# --- Ausführung des Web-Scrapers ---
fetcher = ArticleFetcher()  # Erstellt eine Instanz der 'ArticleFetcher'-Klasse.
all_articles = fetcher.fetch()  # Ruft die 'fetch'-Methode auf, um alle Artikel abzurufen und in der Variable 'all_articles' zu speichern.

# --- Ausgabe der gescrapten Daten ---
print("--- Extrahierte Artikel-Informationen ---")
for article in all_articles:
    print(f"Artikel-Objekt: {article}")  # Gibt die standardmäßige String-Darstellung des Article-Objekts aus (dank __repr__).
    print(f"  Titel: {article.title}")  # Gibt den Titel des aktuellen Artikels aus.
    print(f"  Bild-URL: {article.image}")  # Gibt die vollständige, absolute URL des Bildes aus.
    print("-" * 30) # Trennlinie für bessere Lesbarkeit