import requests  # Importiert das 'requests'-Modul für HTTP-Anfragen (zum Abrufen von Webseiten).
from bs4 import BeautifulSoup  # Importiert 'BeautifulSoup' zum Parsen von HTML-Inhalten.
from urllib.parse import urljoin  # Importiert 'urljoin', um relative URLs in absolute URLs umzuwandeln.
import time  # Importiert 'time' für kurze Pausen zwischen den Anfragen, um den Server nicht zu überlasten.
import csv  # Importiert das 'csv'-Modul, das Funktionen zum Lesen und Schreiben von CSV-Dateien bereitstellt.


# %%
class CrawledArticle():
    # Diese Klasse dient als Datencontainer für die Informationen eines jeden gescrapten Artikels.
    def __init__(self, title, emoji, content, image):
        self.title = title    # Der Titel des Artikels.
        self.emoji = emoji    # Das Emoji, das den Artikel begleitet.
        self.content = content  # Der Textinhalt des Artikels.
        self.image = image    # Die absolute URL des Artikelbildes.

    # Die __repr__-Methode ist in diesem Fall nicht streng notwendig für die Funktionalität,
    # da die Objekte direkt in die CSV geschrieben werden und nicht mehr auf der Konsole ausgegeben werden.
    # Sie ist aber nützlich für Debugging, falls man die Objekte doch mal printen möchte.
    def __repr__(self):
        return f"CrawledArticle(Titel: '{self.title}', Emoji: '{self.emoji}')"


class ArticleFetcher():
    # Diese Klasse ist für das Abrufen und Parsen der Artikel von der Webseite zuständig,
    # inklusive der Navigation über mehrere Seiten hinweg.
    def fetch(self):
        url = "http://python.beispiel.programmierenlernen.io/index.php"  # Die Start-URL für den Crawler.
        articles = []  # Eine leere Liste, um alle gesammelten Artikel zu speichern.

        # Eine Schleife, die so lange läuft, wie 'url' einen gültigen Wert hat.
        # Sie stoppt, wenn keine "Nächste Seite"-Schaltfläche mehr gefunden wird.
        while url != "":
            print(f"Besuche URL: {url}")  # Zeigt die aktuell besuchte URL an (zur Information).
            time.sleep(1)  # Kurze Pause, um den Server nicht zu überlasten.

            r = requests.get(url)  # Sendet eine HTTP GET-Anfrage an die aktuelle URL.
            doc = BeautifulSoup(r.text, "html.parser")  # Parsen des HTML-Inhalts der Antwort.

            # Iteriert über jedes HTML-Element mit der CSS-Klasse "card" auf der aktuellen Seite.
            for card in doc.select(".card"):
                emoji = card.select_one(".emoji").text  # Extrahiert das Emoji.
                content = card.select_one(".card-text").text  # Extrahiert den Artikeltext.
                title = card.select(".card-title span")[1].text  # Extrahiert den Titel.
                # Extrahiert die Bild-URL und wandelt sie in eine absolute URL um.
                image = urljoin(url, card.select_one("img").attrs["src"])

                # Erstellt ein CrawledArticle-Objekt und fügt es der Gesamtliste hinzu.
                crawled = CrawledArticle(title, emoji, content, image)
                articles.append(crawled)

            # Sucht nach dem "Zur nächsten Seite"-Button.
            next_button = doc.select_one(".navigation .btn")

            # Überprüft, ob ein "Nächste Seite"-Button gefunden wurde.
            if next_button:
                next_href = next_button.attrs["href"]  # Holt den relativen Link der nächsten Seite.
                next_href = urljoin(url, next_href)  # Wandelt ihn in eine absolute URL um.
                url = next_href  # Setzt die URL für den nächsten Schleifendurchlauf.
            else:
                url = ""  # Wenn kein Button gefunden, setze URL leer, um die Schleife zu beenden.

        return articles  # Gibt die vollständige Liste aller gesammelten Artikel zurück.


# --- Hauptausführung: Artikel abrufen und in CSV speichern ---

fetcher = ArticleFetcher()  # Erstellt eine Instanz des ArticleFetchers.

# Öffnet eine Datei namens 'crawler_output.csv' im Schreibmodus ('w').
# 'newline=''' ist wichtig, um leere Zeilen zwischen den Datensätzen in Windows zu vermeiden.
with open('crawler_output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Erstellt ein CSV-Writer-Objekt.
    # delimiter=';': Trennt Spalten mit einem Semikolon.
    # quotechar='"': Verwendet doppelte Anführungszeichen, um Felder zu umschließen, die das Trennzeichen enthalten.
    # quoting=csv.QUOTE_MINIMAL: Schließt Felder nur dann in Anführungszeichen ein, wenn sie Sonderzeichen (wie das Trennzeichen) enthalten.
    articlewriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Optional: Schreibe eine Kopfzeile in die CSV-Datei, damit die Spaltenbezeichnungen klar sind.
    articlewriter.writerow(['Emoji', 'Titel', 'Bild-URL', 'Inhalt'])

    # Ruft die fetch()-Methode auf, um alle Artikel zu sammeln.
    # Iteriert dann über jeden gesammelten Artikel.
    for article in fetcher.fetch():
        # Schreibt eine Zeile in die CSV-Datei für jeden Artikel.
        # Die Reihenfolge der Daten entspricht der Kopfzeile.
        articlewriter.writerow([article.emoji, article.title, article.image, article.content])

print("\nDaten erfolgreich in 'crawler_output.csv' gespeichert.")

"""
Was in welcher Reihenfolge passiert (Schwerpunkt CSV-Export)

    Vorbereitung (Imports und Klassen-Definitionen):
        Alle notwendigen Bibliotheken (requests, BeautifulSoup, urljoin, time, und neu: csv) werden importiert.
        Die Klassen CrawledArticle und ArticleFetcher werden wie gehabt definiert. Ihre Aufgabe ist es, die Daten zu holen und als Objekte zu strukturieren. Die Logik zur Paginierung bleibt unverändert in der fetch()-Methode.

    Initialisierung des Crawling-Prozesses:
        Am Ende des Skripts wird eine Instanz von ArticleFetcher erstellt: fetcher = ArticleFetcher().

    Öffnen und Vorbereiten der CSV-Datei:
        with open('crawler_output.csv', 'w', newline='', encoding='utf-8') as csvfile: ist der erste wichtige Schritt für den CSV-Export.
            open(...) versucht, eine Datei namens crawler_output.csv zu öffnen.
            'w' bedeutet, dass die Datei im Schreibmodus geöffnet wird. Wenn die Datei existiert, wird ihr Inhalt gelöscht; wenn nicht, wird sie neu erstellt.
            newline='' ist entscheidend beim Schreiben von CSV-Dateien in Python. Es verhindert, dass zusätzliche Leerzeilen zwischen den Zeilen in der CSV-Datei eingefügt werden, was besonders auf Windows-Systemen passieren könnte.
            encoding='utf-8' stellt sicher, dass Sonderzeichen (wie die Emojis) korrekt in der CSV-Datei gespeichert und später richtig angezeigt werden können.
            as csvfile: weist das geöffnete Dateiobjekt der Variable csvfile zu. Der with-Statement sorgt dafür, dass die Datei automatisch geschlossen wird, sobald der Block verlassen wird, auch wenn Fehler auftreten.
        articlewriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL): Innerhalb des with-Blocks wird ein csv.writer-Objekt erstellt.
            Dieses Objekt ist dafür verantwortlich, Datenzeilen in die csvfile zu schreiben.
            delimiter=';' setzt das Semikolon als Spaltentrenner fest (wichtig für Excel-Kompatibilität in einigen Regionen).
            quotechar='"' legt fest, dass doppelte Anführungszeichen verwendet werden, um Felder zu umschließen, die Sonderzeichen enthalten.
            quoting=csv.QUOTE_MINIMAL ist eine Strategie, die besagt, dass Anführungszeichen nur dann verwendet werden sollen, wenn es unbedingt nötig ist (z.B. wenn ein Feld selbst ein Semikolon enthält).
        articlewriter.writerow(['Emoji', 'Titel', 'Bild-URL', 'Inhalt']): Optional, aber empfohlen! Hier wird eine Kopfzeile in die CSV-Datei geschrieben. Das macht die Datei später viel einfacher zu verstehen, da jede Spalte eine klare Bezeichnung hat.

    Abrufen der Artikel und Schreiben in die CSV-Datei:
        for article in fetcher.fetch():: Hier wird die fetch()-Methode aufgerufen. Wichtig: Die fetch()-Methode wird einmal ausgeführt und gibt dann die komplette Liste aller Artikel von allen Seiten zurück. Die for-Schleife durchläuft dann diese bereits gesammelte Liste.
        articlewriter.writerow([article.emoji, article.title, article.image, article.content]): Für jedes article-Objekt aus der zurückgegebenen Liste wird eine neue Zeile in die CSV-Datei geschrieben. Die Daten (emoji, title, image, content) werden als Liste an writerow() übergeben, wobei jedes Element in der Liste eine Spalte in der CSV-Datei darstellt.

    Abschluss:
        Sobald die for-Schleife alle Artikel verarbeitet hat, wird der with-Block verlassen, und die crawler_output.csv-Datei wird automatisch geschlossen und gespeichert.
        Zuletzt wird eine Bestätigung auf der Konsole ausgegeben, dass die Daten gespeichert wurden.

Nachdem das Skript vollständig ausgeführt wurde, findest du im selben Verzeichnis, in dem dein Python-Skript liegt, eine neue Datei namens crawler_output.csv, die du mit Excel oder einem Texteditor öffnen kannst.

"""