# Das Requests-Modul
# In dieser Lektion lernst du, wie du eine Webseite herunterlädst und ihren HTML-Code anzeigen lassen kannst.
# Dazu verwenden wir das requests-Modul, eine beliebte Bibliothek für HTTP-Anfragen in Python.
# Die offizielle Dokumentation findest du hier: http://docs.python-requests.org/en/master
# Wir werden folgende Seite crawlen (herunterladen): http://python.beispiel.programmierenlernen.io/index.php

import requests # Importiere das requests-Modul, um HTTP-Anfragen zu stellen.

# Führe eine GET-Anfrage an die angegebene URL aus.
# Die Antwort der Webseite wird im 'r'-Objekt gespeichert.
r = requests.get("http://python.beispiel.programmierenlernen.io/index.php")

# Gib das Response-Objekt aus.
# Dies zeigt eine grundlegende Darstellung der Antwort, z.B. "<Response [200]>".
# Die Zahl in den Klammern ist der HTTP-Statuscode.
print(r)

# Gib den HTTP-Statuscode der Antwort aus.
# 200 bedeutet "OK" (die Anfrage war erfolgreich).
# 404 würde "Not Found" bedeuten (die angefragte Seite existiert nicht).
# Es gibt viele weitere Statuscodes, die verschiedene Bedeutungen haben.
print(r.status_code)

# Gib die HTTP-Header der Antwort aus.
# Header enthalten Metadaten über die Antwort, wie z.B. das Datum, den Servertyp,
# den Inhaltstyp (z.B. HTML, JSON), die Zeichenkodierung (charset) und mehr.
# Dies ist nützlich, um Details über die Kommunikation mit dem Server zu erfahren.
print(r.headers)

# Gib den eigentlichen Inhalt der Webseite aus.
# Das 'text'-Attribut des Response-Objekts enthält den HTML-Code der heruntergeladenen Seite
# als String. Dies ist der Rohtext, den ein Webbrowser rendern würde.
print(r.text)

