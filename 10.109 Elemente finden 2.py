import requests  # Importiert das 'requests'-Modul, um HTTP-Anfragen (z.B. Webseiten abrufen) durchführen zu können.
from bs4 import BeautifulSoup  # Importiert 'BeautifulSoup' aus dem 'bs4'-Modul, um HTML- und XML-Dokumente parsen zu
# können.


# %%
class CrawledArticle():  # Definiert eine Klasse namens 'CrawledArticle'.
    def __init__(self, title, emoji, content,
                 image):  # Der Konstruktor der Klasse. Er wird aufgerufen, wenn ein neues 'CrawledArticle'-Objekt erstellt wird.
        self.title = title  # Speichert den übergebenen 'title' als Attribut des Objekts.
        self.emoji = emoji  # Speichert das übergebene 'emoji' als Attribut des Objekts.
        self.content = content  # Speichert den übergebenen 'content' als Attribut des Objekts.
        self.image = image  # Speichert das übergebene 'image' (Bild-URL) als Attribut des Objekts.


class ArticleFetcher():  # Definiert eine Klasse namens 'ArticleFetcher'.
    def fetch(self):  # Definiert eine Methode namens 'fetch' innerhalb der 'ArticleFetcher'-Klasse.
        r = requests.get("http://python.beispiel.programmierenlernen.io/index.php")  # Sendet eine GET-Anfrage an die angegebene URL und speichert die Antwort in der Variablen 'r'.
        doc = BeautifulSoup(r.text,"html.parser")  # Erstellt ein BeautifulSoup-Objekt aus dem Textinhalt der HTTP-Antwort. "html.parser" gibt den Parser an, der verwendet werden soll.

        articles = []  # Initialisiert eine leere Liste, um die extrahierten Artikel zu speichern.
        for card in doc.select(".card"):  # Iteriert über alle HTML-Elemente mit der CSS-Klasse "card", die im Dokument gefunden werden.
            emoji = card.select_one(".emoji").text  # Sucht innerhalb der aktuellen "card" das erste Element mit der Klasse "emoji" und extrahiert dessen Textinhalt.
            content = card.select_one(".card-text").text  # Sucht innerhalb der aktuellen "card" das erste Element mit der Klasse "card-text" und extrahiert dessen Textinhalt.
            title = card.select(".card-title span")[1].text  # Sucht innerhalb der aktuellen "card" alle 'span'-Elemente innerhalb eines Elements mit der Klasse "card-title" und extrahiert den Textinhalt des zweiten 'span'-Elements (Index 1).
            image = card.select_one("img").attrs["src"]  # Sucht innerhalb der aktuellen "card" das erste 'img'-Element und extrahiert den Wert des "src"-Attributs (die Bild-URL).

            crawled = CrawledArticle(title, emoji, content,image)  # Erstellt ein neues 'CrawledArticle'-Objekt mit den extrahierten Daten.
            articles.append(crawled)  # Fügt das erstellte 'CrawledArticle'-Objekt der 'articles'-Liste hinzu.
        return articles  # Gibt die Liste der 'CrawledArticle'-Objekte zurück.


fetcher = ArticleFetcher()  # Erstellt eine Instanz der Klasse 'ArticleFetcher'.
all_articles = fetcher.fetch()  # Hier wird der Rückgabewert in 'all_articles' gespeichert

# Jetzt können wir die Artikel ausgeben
for article in all_articles:
    print(article)  # Jedes Artikel-Objekt wird ausgegeben
"""
Was der Code macht:

Dieser Code ist ein grundlegender Web-Scraper, der Inhalte von der Webseite "http://python.beispiel.programmierenlernen.io/index.php" extrahiert.

    CrawledArticle Klasse: Dies ist eine Datenstruktur, die dazu dient, die Informationen jedes gescrapten Artikels (Titel, Emoji, Inhalt, Bild-URL) sauber zu speichern.
    ArticleFetcher Klasse: Diese Klasse führt die eigentliche Arbeit des Web-Scrapings durch.
        Die fetch-Methode sendet eine HTTP-Anfrage an die angegebene URL.
        Sie parst den HTML-Inhalt der Webseite mit BeautifulSoup.
        Anschließend durchsucht sie den geparsten HTML-Code nach spezifischen Elementen (solche mit den CSS-Klassen .card, .emoji, .card-text, .card-title, und img-Tags), um die relevanten Informationen jedes Artikels zu extrahieren.
        Für jeden gefundenen Artikel wird ein CrawledArticle-Objekt erstellt und zu einer Liste hinzugefügt.
        Am Ende gibt die Methode diese Liste von CrawledArticle-Objekten zurück.

Der letzte Teil des Codes (fetcher = ArticleFetcher(); fetcher.fetch()) erstellt eine Instanz des ArticleFetcher und ruft dessen fetch-Methode auf, um den Scraping-Prozess zu starten. Die zurückgegebenen Artikel werden dann, obwohl sie hier nicht explizit ausgegeben werden, in der Liste articles innerhalb der fetch-Methode gespeichert.

"""
