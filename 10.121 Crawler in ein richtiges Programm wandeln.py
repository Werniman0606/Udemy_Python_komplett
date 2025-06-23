""" Wie wandeln wir das ganze nun in Pycharm in ein ausführbares Programm um ?
Nun,wir legen erstmal ein neues Python-Package an, es erscheint dann ein Ordner,wo schon eine Datei __init__.py drin
liegt. Wir kopieren nun aus unserem Crawler-Code die Klassendefinition und packen ihn in eine neue Python-Datei mit
gleichem Namen in diesen Python-Package-Ordner. Gleiches machen wir mit der Klasse ArticleFetscher
"""

"""
Wie die Dateien miteinander interagieren

Die Stärke deiner aktuellen Struktur liegt in der Modulbildung und der sauberen Trennung von Verantwortlichkeiten. Lass uns die Interaktion Schritt für Schritt durchgehen:
1. Das Crawler-Package (Ordner Crawler/)

    __init__.py: Dies ist die Eintrittspforte deines Packages. Wenn du in crawler.py schreibst import Crawler, sucht Python nach dem Ordner Crawler/ und führt als Erstes die __init__.py-Datei darin aus.
        Ihre Hauptaufgabe ist es, ArticleFetcher und CrawledArticle für den direkten Import im Package-Namespace verfügbar zu machen. Das bedeutet, anstatt Crawler.ArticleFetcher.ArticleFetcher zu schreiben, kannst du einfach Crawler.ArticleFetcher nutzen.
        Die __all__-Liste definiert explizit, welche Namen exportiert werden, wenn jemand from Crawler import * verwenden würde. Das ist eine gute Praxis zur Kontrolle der API des Packages.

    ArticleFetcher.py: Dies ist das "Gehirn" des Crawling-Prozesses.
        Es enthält die ArticleFetcher-Klasse, deren Hauptmethode fetch() ist.
        Abhängigkeit von CrawledArticle.py: ArticleFetcher.py importiert from .CrawledArticle import CrawledArticle. Das bedeutet, dass ArticleFetcher die Definition der CrawledArticle-Klasse benötigt, um die gecrawlten Daten in ein strukturiertes Format zu bringen. Es erstellt Instanzen von CrawledArticle, nachdem es die Daten von der Webseite extrahiert hat.
        Die fetch()-Methode ist als Generator implementiert. Das ist ein Schlüsselelement der Interaktion: Sie gibt nicht alle Artikel auf einmal zurück, sondern "liefert" sie einzeln, sobald sie gefunden und geparst wurden. Dies ist sehr speichereffizient, besonders bei vielen Artikeln.

    CrawledArticle.py: Dies ist der "Datenhalter".
        Es definiert die einfache CrawledArticle-Klasse. Diese Klasse ist ein Passivobjekt, das heißt, sie enthält hauptsächlich Daten (Titel, Emoji, Inhalt, Bild-URL) und hat keine komplexe Logik.
        Sie dient als Standardformat für die gecrawlten Artikel. ArticleFetcher "produziert" Objekte dieses Typs, und andere Teile deines Programms (wie crawler.py) "konsumieren" sie.

2. Das Hauptskript: crawler.py

    Import des Packages: import Crawler bindet das gesamte Package ein und macht dessen Inhalte (wie ArticleFetcher) zugänglich.
    Initialisierung: fetcher = Crawler.ArticleFetcher() erstellt eine Instanz des ArticleFetcher. An diesem Punkt wird noch nichts gecrawlt. Es wird lediglich ein Objekt vorbereitet, das später den Crawling-Prozess starten kann.
    Konsumieren des Generators: Die Zeile for element in fetcher.fetch(): ist das Herzstück der Interaktion.
        Sie ruft die fetch()-Methode auf, die, wie oben erwähnt, ein Generator ist.
        Die for-Schleife beginnt, Artikel vom Generator anzufordern. Jedes Mal, wenn fetch() ein yield CrawledArticle(...) ausführt, wird dieses CrawledArticle-Objekt zum element in der for-Schleife.
        Die Schleife verarbeitet jeden Artikel einzeln, sobald er verfügbar ist, und gibt dessen Emoji und Titel aus. Dies zeigt, dass die Daten erfolgreich von der Webseite abgerufen, geparst und in das definierte CrawledArticle-Format überführt wurden.

Zusammenfassend: Der Datenfluss

    Die Anwendung (crawler.py) startet.
    Sie lädt das Crawler-Package, wodurch ArticleFetcher und CrawledArticle im Package-Namespace verfügbar werden.
    Eine ArticleFetcher-Instanz wird erstellt.
    Die for-Schleife in crawler.py ruft die fetch()-Methode des ArticleFetcher auf.
    Der ArticleFetcher beginnt, Webseiten zu besuchen, HTML zu parsen und Artikeldaten zu extrahieren.
    Für jeden gefundenen Artikel erstellt der ArticleFetcher ein CrawledArticle-Objekt und yield dieses.
    Die for-Schleife in crawler.py empfängt das CrawledArticle-Objekt und verarbeitet es sofort (gibt Emoji und Titel aus).
    Dieser Prozess wiederholt sich, bis alle paginierten Seiten durchsucht und alle Artikel verarbeitet wurden.

Diese Struktur bietet eine saubere Trennung von Bedenken (Separation of Concerns): Das Package kümmert sich um das technische Crawling und die Datenstruktur, während das Hauptskript die Anwendung orchestriert und die Ergebnisse nutzt. Das macht deinen Code wartbarer, lesbarer und wiederverwendbar.
"""

