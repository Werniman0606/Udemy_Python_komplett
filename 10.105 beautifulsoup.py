# Elemente in HTML finden
#
# In dieser Lektion lernst du, wie du Informationen aus einer HTML-Datei extrahieren kannst.
# Dafür nutzen wir die leistungsstarke Bibliothek BeautifulSoup (mehr dazu unter: https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
# BeautifulSoup hilft uns, den HTML-Code zu "zerlegen" und ihn so zu strukturieren, dass wir leicht auf einzelne Elemente zugreifen können.

# ---
## 1. Eine Webseite abrufen (Optional für echte Web-Scraping-Szenarien)
# ---

import requests

# Zuerst simulieren wir den Abruf einer echten Webseite. In einem realen Szenario würdest du hier eine URL angeben,
# von der du Daten "scrapen" möchtest. Das 'requests'-Modul sendet eine HTTP GET-Anfrage an die angegebene URL.
r = requests.get("http://python.beispiel.programmierenlernen.io/index.php")
# Das 'r'-Objekt enthält die Antwort der Anfrage, einschließlich des HTML-Codes der Seite.

# ---
## 2. HTML-Code vorbereiten
# ---

from bs4 import BeautifulSoup

# Für die Demonstration und zum einfachen Testen arbeiten wir oft mit einem direkt im Code definierten HTML-String.
# Hier ist ein einfaches Beispiel:
html = "<html><body><p>Ich bin ein Absatz</p></body></html>"

# Wenn der HTML-Code komplexer ist und mehrere Zeilen umfasst, verwenden wir drei Anführungszeichen (dreifache Anführungszeichen)
# um einen mehrzeiligen String zu definieren. Das macht den Code viel übersichtlicher, da du den HTML-Code einrücken kannst.
html = """
    <html>
        <body>
            <p class="something">
            Ich bin ein Absatz
            </p>
            <p>
            Ich bin noch ein Absatz!
            </p>
        </body>
    </html>
"""

# ---
## 3. HTML mit BeautifulSoup parsen
# ---

# Jetzt übergeben wir unseren HTML-Code an BeautifulSoup, um ihn zu "parsen".
# Der erste Parameter ist der HTML-String, den wir analysieren möchten.
# Der zweite Parameter, "html.parser", weist BeautifulSoup an, den standardmäßigen Python-HTML-Parser zu verwenden.
# Das Ergebnis ist ein 'BeautifulSoup'-Objekt ('doc'), das den HTML-Code als Baumstruktur darstellt,
# was die Navigation und Suche nach Elementen sehr einfach macht.
doc = BeautifulSoup(html, "html.parser")

# ---
## 4. Elemente finden
# ---

# Die Methode 'find_all("p")' sucht im gesamten geparsten Dokument nach allen HTML-Elementen, die das Tag '<p>' haben.
# Sie gibt eine Liste von 'Tag'-Objekten zurück, wobei jedes Objekt ein gefundenes Absatz-Element repräsentiert.
print(doc.find_all("p"))
# Erwartete Ausgabe:
# [<p class="something">
#             Ich bin ein Absatz
#             </p>, <p>
#             Ich bin noch ein Absatz!
#             </p>]
# Beachte, dass BeautifulSoup die Struktur und Attribute der Tags beibehält.

# ---
## 5. Durch gefundene Elemente iterieren und Informationen extrahieren
# ---

# Wir können eine Schleife verwenden, um über jedes gefundene <p>-Element zu iterieren.
for p in doc.find_all("p"):
    # 'p.attrs' gibt ein Python-Dictionary zurück, das alle Attribute des aktuellen HTML-Tags enthält.
    # Zum Beispiel hat der erste Absatz das Attribut 'class' mit dem Wert 'something'.
    # Der zweite Absatz hat keine Attribute, daher ist sein Dictionary leer.
    print(p.attrs)
    # 'p.text' extrahiert den reinen Textinhalt innerhalb des HTML-Tags, ohne die Tags selbst.
    # Dies ist sehr nützlich, um den sichtbaren Text aus einem Element zu erhalten.
    print(p.text)
    # Erwartete Ausgabe für jedes <p>-Element:
    # {'class': ['something']}  (für den ersten Absatz)
    # Ich bin ein Absatz
    #
    # {}  (für den zweiten Absatz)
    # Ich bin noch ein Absatz!