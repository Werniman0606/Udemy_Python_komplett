"""
## Python Wissen: Generatoren

In dieser Lektion geht's um ein weiteres Python-Konzept, welches unseren Crawler etwas vereinfachen kann: Generatoren.

Problem: Manchmal interessieren dich nur die ersten 5 Einträge, manchmal möchtest du alle Einträge einlesen. Wie bekommen wir es hin, dass die .fetch()-Methode automatisch erkennt, wie viele Einträge mich interessieren?

In dieser Lektion lernst du:

- Was Generatoren sind
- Und wie du diese in Python verwenden kannst.

"""

# Bisher hätten wir eine Liste über eine Funktion wie folgt generiert und ausgegeben
def gen_list():
    # Initialisiert eine leere Liste.
    liste = []
    # Beginnt eine Schleife, die von 0 bis 9 (insgesamt 10 Iterationen) läuft.
    for i in range(0, 10):
        # Gibt eine Nachricht aus, die zeigt, welcher Wert gerade zur Liste hinzugefügt wird.
        # Diese print-Anweisung wird FÜR ALLE Iterationen ausgeführt, BEVOR die Liste zurückgegeben wird.
        print("liste: " + str(i))
        # Fügt den aktuellen Wert 'i' zur Liste hinzu.
        liste.append(i)
    # Nachdem die Schleife komplett durchlaufen wurde, gibt die Funktion die VOLLSTÄNDIGE Liste zurück.
    return liste


# Die 'gen_list()'-Funktion wird HIER aufgerufen und gibt die komplette Liste zurück.
# Erst DANACH beginnt die 'for'-Schleife über die zurückgegebene Liste zu iterieren.
for element in gen_list():
    # Gibt jeden 'element' aus der bereits vollständig erzeugten Liste aus.
    print("for: " + str(element))

"""Ausgabe
liste: 0
liste: 1
liste: 2
liste: 3
liste: 4
liste: 5
liste: 6
liste: 7
liste: 8
liste: 9
for: 0
for: 1
for: 2
for: 3
for: 4
for: 5
for: 6
for: 7
for: 8
for: 9


Erklärung:
Die Funktion gen_list() läuft komplett durch, baut die gesamte Liste im Speicher auf und gibt sie dann als Ganzes 
zurück. Erst nachdem gen_list() vollständig abgeschlossen ist, beginnt die for-Schleife, über diese fertige Liste zu 
iterieren. Dies ist der typische Weg, wie Python-Funktionen Listen oder andere Datenstrukturen zurückgeben.    """
print("##########################################")


def gen_generator():
    # Beginnt eine Schleife, die von 0 bis 9 läuft.
    for i in range(0, 10):
        # Gibt eine Nachricht aus, die zeigt, welcher Wert als Nächstes "erzeugt" wird.
        print("gen: " + str(i))
        # 'yield' ist das Schlüsselwort, das eine Funktion zu einem Generator macht.
        # Wenn 'yield' erreicht wird, gibt der Generator den aktuellen Wert 'i' zurück
        # und PAUSIERT seine Ausführung an dieser Stelle.
        # Er merkt sich seinen Zustand und setzt die Ausführung fort,
        # wenn das nächste Element angefordert wird.
        yield i


# Die 'gen_generator()'-Funktion wird HIER aufgerufen, gibt aber nicht sofort alle Werte zurück.
# Stattdessen gibt sie ein Generator-Objekt zurück.
# Die 'for'-Schleife fordert dann ITERATIV die Werte vom Generator an.
for element in gen_generator():
    # Diese print-Anweisung wird AUSGEFÜHRT, NACHDEM ein Wert vom Generator erzeugt und empfangen wurde.
    print("for: " + str(element))

"""
gen: 0
for: 0
gen: 1
for: 1
gen: 2
for: 2
gen: 3
for: 3
gen: 4
for: 4
gen: 5
for: 5
gen: 6
for: 6
gen: 7
for: 7
gen: 8
for: 8
gen: 9
for: 9

Erklärung:
Die gen_generator()-Funktion wird zu einem Generator, weil sie das Schlüsselwort yield verwendet. Wenn du gen_generator() aufrufst, gibt sie nicht sofort alle Werte zurück, sondern ein Generator-Objekt. Die for-Schleife fordert dann bei jedem Durchlauf den nächsten Wert vom Generator an.

    Wenn yield i erreicht wird, gibt der Generator i zurück und pausiert.
    Die for-Schleife empfängt i und führt print("for: " + str(element)) aus.
    Erst wenn die for-Schleife den nächsten Wert anfordert, setzt der Generator seine Ausführung genau an der Stelle fort, an der er pausiert hat, und läuft bis zum nächsten yield (oder bis zum Ende der Funktion).

Dieser "on-the-fly"-Ansatz spart Speicher, da nicht alle Werte gleichzeitig erzeugt und gespeichert werden müssen."""

print("##########################################")


def gen_generator():
    # Dieselbe Generatorfunktion wie zuvor.
    for i in range(0, 10):
        print("gen: " + str(i))
        yield i


# Die 'for'-Schleife iteriert über den Generator.
for element in gen_generator():
    # Eine Bedingung wird geprüft. Wenn 'element' 4 ist, wird die Schleife beendet.
    if element == 4:
        # 'break' beendet die for-Schleife VORZEITIG.
        # Da die for-Schleife die einzige Anforderung an den Generator ist,
        # wird der Generator an dieser Stelle ebenfalls seine Ausführung einstellen.
        break
    # Gibt den Wert aus, falls die break-Bedingung nicht erfüllt ist.
    print("for: " + str(element))
"""Ausgabe:
gen: 0
for: 0
gen: 1
for: 1
gen: 2
for: 2
gen: 3
for: 3
gen: 4
Erklärung:
Dieser Block demonstriert einen großen Vorteil von Generatoren: Faulheit (Lazy Evaluation) und die Möglichkeit, frühzeitig abzubrechen.

    Der Generator gen_generator() wird gestartet.
    Er erzeugt 0 (gen: 0) und gibt ihn an die for-Schleife. Die Schleife gibt 0 aus.
    Er erzeugt 1 (gen: 1) und gibt ihn an die for-Schleife. Die Schleife gibt 1 aus.
    ...bis er 4 erzeugt (gen: 4).
    Die for-Schleife empfängt 4. Die if element == 4:-Bedingung ist nun True.
    Das break-Statement wird ausgeführt. Dies beendet die for-Schleife.
    Der Generator gen_generator() hört an dieser Stelle ebenfalls auf zu produzieren! Er läuft nicht bis gen: 9 durch, weil keine weiteren Elemente angefordert werden.

Das ist der Schlüssel zur Effizienz: Wenn dein Crawler Hunderte von Seiten hat, du aber nur die ersten 5 Artikel benötigst, kann ein Generator die ersten 5 Artikel abrufen und dann aufhören, anstatt alle Artikel von allen Seiten unnötigerweise zu laden und zu parsen.
"""

"""Generatoren und unser Crawler

Die fetch()-Methode in deinem ArticleFetcher gibt aktuell eine komplette Liste zurück (return articles). Um sie in einen Generator umzuwandeln, müsstest du das articles.append(crawled) und return articles durch ein yield crawled ersetzen.

Das würde bedeuten, dass die fetch()-Methode selbst nicht mehr die ganze Liste im Speicher vorhält, sondern jeden CrawledArticle einzeln "yieldet", sobald er gefunden wird. Dein Code, der die Artikel konsumiert (z.B. die for-Schleife, die sie in die CSV schreibt), könnte dann so aussehen:
fetcher = ArticleFetcher()

with open('crawler_output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    articlewriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    articlewriter.writerow(['Emoji', 'Titel', 'Bild-URL', 'Inhalt'])

    # fetcher.fetch() ist jetzt ein Generator!
    # Die Schleife holt sich Artikel EINEN NACH DEM ANDEREN vom Generator.
    for article in fetcher.fetch():
        articlewriter.writerow([article.emoji, article.title, article.image, article.content])

        # Wenn du jetzt z.B. nur die ersten 5 Artikel in der CSV haben willst, könntest du hier einbrechen:
        # if article.title == "Titel des 5. Artikels" (oder einfacher mit einem Zähler)
        # count += 1
        # if count >= 5:
        #     break
"""
import requests  # Importiert das 'requests'-Modul für HTTP-Anfragen.
from bs4 import BeautifulSoup  # Importiert 'BeautifulSoup' zum Parsen von HTML-Inhalten.
from urllib.parse import urljoin  # Importiert 'urljoin' zum Erstellen absoluter URLs.
import time  # Importiert 'time' für Pausen, um Server zu schonen.
import csv  # Importiert das 'csv'-Modul für den CSV-Export.


# %%
class CrawledArticle():
    # Datencontainer für einen Artikel.
    def __init__(self, title, emoji, content, image):
        self.title = title
        self.emoji = emoji
        self.content = content
        self.image = image

    # Repräsentation des Objekts für lesbare Ausgaben.
    def __repr__(self):
        return f"CrawledArticle(Titel: '{self.title}', Emoji: '{self.emoji}')"


class ArticleFetcher():
    # Diese Klasse ruft Artikel von Webseiten ab, inklusive Paginierung.
    # Die fetch-Methode ist hier als GENERATOR implementiert.
    def fetch(self):
        url = "http://python.beispiel.programmierenlernen.io/index.php"  # Start-URL.

        # Die Schleife läuft so lange, wie eine gültige URL für die nächste Seite existiert.
        while url != "":
            print(f"Besuche URL (Generator): {url}")  # Aktuelle URL wird ausgegeben.
            time.sleep(1)  # Kurze Pause.

            r = requests.get(url)  # HTTP-Anfrage senden.
            doc = BeautifulSoup(r.text, "html.parser")  # HTML parsen.

            # Iteriert über jede "card" auf der aktuellen Seite (jeder Artikel).
            for card in doc.select(".card"):
                emoji = card.select_one(".emoji").text
                content = card.select_one(".card-text").text
                title = card.select(".card-title span")[1].text
                image = urljoin(url, card.select_one("img").attrs["src"])

                crawled = CrawledArticle(title, emoji, content, image)
                # <<< WICHTIGE ÄNDERUNG HIER: 'yield' statt 'articles.append' >>>
                # Der Generator "produziert" einen Artikel und pausiert seine Ausführung.
                # Der Aufrufer (die for-Schleife im Hauptteil) erhält den Artikel sofort.
                yield crawled

            # Logik für die "Nächste Seite"-Schaltfläche.
            next_button = doc.select_one(".navigation .btn")
            if next_button:
                next_href = next_button.attrs["href"]
                next_href = urljoin(url, next_href)
                url = next_href  # URL für den nächsten Schleifendurchlauf setzen.
            else:
                url = ""  # Letzte Seite erreicht, Schleife beenden.

        # WICHTIG: Kein 'return articles' mehr, da die Artikel einzeln ge-yieldet werden.


# --- Hauptausführung: Artikel mit Generator abrufen und in CSV speichern ---

fetcher = ArticleFetcher()  # Erstellt eine Instanz des ArticleFetchers.

# Öffnet die CSV-Datei zum Schreiben.
# 'newline=''' verhindert leere Zeilen. 'encoding='utf-8'' für Sonderzeichen/Emojis.
with open('crawler_output_generator.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Erstellt ein CSV-Writer-Objekt mit Semikolon als Trenner.
    articlewriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Optional: Schreibe eine Kopfzeile in die CSV-Datei.
    articlewriter.writerow(['Emoji', 'Titel', 'Bild-URL', 'Inhalt'])

    # <<< WICHTIGE ÄNDERUNG HIER: for-Schleife direkt über den Generator >>>
    # fetcher.fetch() gibt jetzt ein Generator-Objekt zurück.
    # Die for-Schleife fordert nacheinander Artikel vom Generator an.
    # Der Generator läuft immer nur so weit, wie Artikel benötigt werden.
    # Wenn die Schleife (z.B. durch ein 'break') frühzeitig endet, stoppt auch der Generator.
    for article in fetcher.fetch():
        # Schreibt jeden erhaltenen Artikel sofort als Zeile in die CSV-Datei.
        articlewriter.writerow([article.emoji, article.title, article.image, article.content])

        # Beispiel: Wenn du nur die ersten 5 Artikel speichern möchtest, könntest du hier einen Zähler verwenden:
        # counter = getattr(fetcher, '_counter', 0) # Erster Aufruf: counter = 0
        # fetcher._counter = counter + 1
        # if fetcher._counter >= 5:
        #     print("Nur die ersten 5 Artikel gespeichert. Generator wird beendet.")
        #     break # Beendet die Schleife und somit die Ausführung des Generators
        # Hinweis: Ein Zähler als Attribut des fetcher-Objekts ist hier nur ein Beispiel.
        # Man könnte den Zähler auch außerhalb der Schleife definieren.

print("\nDaten erfolgreich mit Generator in 'crawler_output_generator.csv' gespeichert.")

"""
Erläuterung der Generator-spezifischen Änderungen

    In ArticleFetcher.fetch():
        Die Zeile articles = [] (Initialisierung einer Liste zum Sammeln der Artikel) wurde entfernt.
        Die Zeile articles.append(crawled) wurde durch yield crawled ersetzt. Dies ist der entscheidende Punkt, der fetch() zu einer Generatorfunktion macht. Jedes Mal, wenn yield erreicht wird, wird der Wert (crawled) an den Aufrufer zurückgegeben, und die Funktion pausiert ihren Zustand, bis der nächste Wert angefordert wird.
        Die Zeile return articles am Ende der fetch()-Methode wurde entfernt, da ein Generator keine Liste zurückgibt, sondern Werte nacheinander "yieldet".

    Im Hauptausführungsblock:
        Der Aufruf fetcher.fetch() gibt jetzt direkt ein Generator-Objekt zurück.
        Die for-Schleife (for article in fetcher.fetch():) iteriert nun direkt über dieses Generator-Objekt. Das bedeutet, dass die fetch()-Methode nicht zuerst komplett durchläuft, um eine Liste zu erstellen. Stattdessen wird die fetch()-Methode jedes Mal nur so weit ausgeführt, bis sie einen Artikel yieldt. Dann pausiert sie, bis der nächste Artikel von der for-Schleife angefordert wird.
        Der Kommentar zum break-Statement (aus deinem Beispielcode für Generatoren) wurde als Beispiel hinzugefügt, um zu zeigen, wie du die Datenerfassung mit einem Generator effizient abbrechen könntest, wenn du nur eine bestimmte Anzahl von Elementen benötigst.

Mit dieser Generator-basierten Implementierung ist dein Crawler speichereffizienter, insbesondere bei sehr vielen Seiten, da nicht alle Artikel gleichzeitig im RAM gehalten werden müssen. Die Daten werden "on the fly" verarbeitet und direkt in die CSV-Datei geschrieben.

"""
