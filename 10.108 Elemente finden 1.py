# Titel: Elemente in HTML finden
# Beschreibung: In dieser Lektion lernst du, wie du aus einer HTML-Datei Informationen extrahieren kannst.
# Dafür nutzen wir die leistungsstarke Bibliothek BeautifulSoup.
# Weitere Informationen zu BeautifulSoup findest du unter: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# BeautifulSoup hilft uns, den HTML-Code zu "zerlegen" und ihn so zu strukturieren,
# dass wir leicht auf einzelne Elemente zugreifen können.

# Zuerst holen wir uns den Inhalt der Webseite, die eingelesen werden soll.
# Die 'requests'-Bibliothek wird verwendet, um HTTP-Anfragen zu stellen (z.B. eine Webseite herunterzuladen).
import requests

# Eine GET-Anfrage an die angegebene URL senden, um den HTML-Inhalt der Seite zu erhalten.
r = requests.get("http://python.beispiel.programmierenlernen.io/index.php")

# Die 'BeautifulSoup'-Bibliothek wird importiert, um den HTML-Inhalt zu parsen.
from bs4 import BeautifulSoup

# Ein BeautifulSoup-Objekt erstellen.
# 'r.text' enthält den gesamten HTML-Inhalt der heruntergeladenen Seite.
# "html.parser" ist der Parser, der BeautifulSoup mitteilt, wie der HTML-Code interpretiert werden soll.
doc = BeautifulSoup(r.text, "html.parser")

# Wenn wir die Seite im Browser geöffnet haben und uns eine Überschrift eines Absatzes markieren
# und mit Rechtsklick auf "Inspect" gehen, sehen wir, dass die einzelnen Abschnitte
# immer mit dem Code <div class="card"> beginnen.
# Wir verwenden '.select(".card")', um alle HTML-Elemente zu finden, die die CSS-Klasse "card" besitzen.
# Dies gibt eine Liste von BeautifulSoup-Tag-Objekten zurück, wobei jedes Objekt eine Karte repräsentiert.
for card in doc.select(".card"):
    # Der folgende Code zeigt, wie man den gesamten HTML-Inhalt einer einzelnen Karte ausgeben kann.
    # print(card)
    # Beispielausgabe (gekürzt):
    """
    <div class="card">
        <div class="card-block">
            <a href="./img/1.jpg" target="_blank">
                <img alt="Bild 1" class="img-responsive float-right" src="./img/1.jpg" style="max-height: 100px; max-width:110px; margin-left:15px;" />
            </a>
            <h4 class="card-title">
                <span class="emoji">😩</span>
                <span>Polarised modular conglomeration</span>
    ........ (abgekürzt, die Ausgabe ist deutlich länger)
    """

    # Der folgende Code zeigt, wie man alle Elemente mit der Klasse "emoji" innerhalb einer Karte finden kann.
    # Dies gibt eine Liste von Tag-Objekten zurück, selbst wenn es nur eines ist.
    # print(card.select(".emoji"))
    # Beispielausgabe für eine einzelne Karte:
    """
    [<span class="emoji">😩</span>]
    """

    # Um nur den Text des Emojis zu erhalten, wählen wir das erste (und in diesem Fall einzige)
    # Element mit der Klasse "emoji" aus und greifen auf dessen Textinhalt zu.
    # '.select_one(".emoji")' wählt das erste passende Element aus.
    # '.text' extrahiert den sichtbaren Textinhalt des HTML-Elements.
    # Das Problem: Wenn wir dies außerhalb der Schleife tun würden, würde es ALLE Emojis auf einer Seite ausgeben.
    # Innerhalb der Schleife greifen wir jedoch auf das Emoji *pro Karte* zu.
    emoji = card.select_one(".emoji").text
    print(emoji)

    # Als Nächstes wollen wir den eigentlichen Text ("Optio numquam ut accusantium laborum...") holen.
    # Im HTML-Code ist dieser Text in einem <p>-Tag mit der Klasse "card-text" enthalten.
    # Wir verwenden '.select_one(".card-text")' um dieses Element zu finden und '.text',
    # um seinen Inhalt zu extrahieren.
    content = card.select_one(".card-text").text
    print(content)

    # Der Titel ist in einer Liste innerhalb des Typs 'card-title' versteckt und ist dort vom Typ <span>.
    # Es ist das zweite <span>-Objekt innerhalb des 'card-title'-Elements.
    # Da '.select()' eine Liste von Elementen zurückgibt, können wir über den Index direkt darauf zugreifen.
    # '[1]' greift auf das zweite Element der Liste zu (Index 0 ist das erste Element, Index 1 das zweite).
    title = card.select(".card-title span")[1].text
    print(title)

    # Und was ist mit unserem Bild? Die entsprechende Zeile ist diese hier:
    # <img class="img-responsive float-right" src="./img/1.jpg" style="max-height: 100px;max-width:110px;margin-left:15px;" alt="Bild 1">
    # Wir wählen das 'img'-Tag innerhalb der aktuellen Karte aus.
    # 'image' wird als BeautifulSoup-Tag-Objekt gespeichert, das die Attribute des <img>-Tags enthält.
    image = card.select_one("img")
    # Die Attribute eines Tags können über das '.attrs'-Dictionary abgerufen werden.
    # Wir geben den Wert des Attributs "src" aus, das den Pfad zum Bild enthält.
    print(image.attrs["src"])

    # 'break' beendet die Schleife nach dem ersten Durchlauf.
    # Dies ist nützlich, wenn man nur die Daten der ersten Karte verarbeiten möchte.
    break
    # Beispielausgabe nach dem ersten Schleifendurchlauf (wegen 'break'):
    # 😩
    # Optio numquam ut accusantium laborum unde assumenda. Ea et totam asperiores fugiat voluptatem vitae. Et provident nam et mollitia.
    # Polarised modular conglomeration
    # ./img/1.jpg
