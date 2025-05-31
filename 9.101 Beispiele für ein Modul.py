# --- Einführung in das `csv`-Modul von Python ---

# In dieser Lektion erkunden wir das eingebaute `csv`-Modul von Python,
# das speziell für die Arbeit mit CSV-Dateien (Comma Separated Values) entwickelt wurde.
# Eine vollständige Liste aller von Python unterstützten Module findest du unter:
# https://docs.python.org/3/py-modindex.html

# Wir werden anhand eines Beispiels demonstrieren, wie du mit diesem Modul
# komfortabel Daten aus einer CSV-Datei lesen kannst.

# Angenommener Inhalt der Datei 'datei.csv' (liegt im selben Verzeichnis):
# Muenchen;1800000;MUC

# Das `csv`-Modul importieren
import csv

# --- Öffnen und Lesen der CSV-Datei (Standardfall) ---

# Öffnen der Datei 'datei.csv' im Lesemodus ('r')
# 'newline=''' ist wichtig, um Probleme mit Zeilenumbrüchen zu vermeiden,
# besonders unter Windows. Es verhindert, dass Leerzeilen zwischen den Daten entstehen.
with open('datei.csv', newline='') as file:
    # Erstellen eines `csv.reader`-Objekts
    # Wir geben den verwendeten Trenner (delimiter) an, da unsere Datei Semikolons (;) verwendet
    # und nicht das Standard-Komma.
    spamreader = csv.reader(file, delimiter=';')

    # Iterieren über jede Zeile im Reader-Objekt
    # Jede 'line' ist eine Liste von Strings, die die Spalten der aktuellen Zeile repräsentiert.
    for line in spamreader:
        print(line)
        # Beispiel-Ausgabe für die Zeile "Muenchen;1800000;MUC":
        # ['Muenchen', '1800000', 'MUC']

---
# --- Umgang mit Trennzeichen innerhalb von Datenfeldern (quotechar) ---

# Was passiert, wenn ein Trennzeichen (z.B. ein Semikolon) *selbst* Teil eines Datenfeldes ist
# und nicht als Spaltentrenner interpretiert werden soll?
#
# Beispiel für ein Problem:
# Hamburg;Harburg;800000;HAM  <-- Hier würde "Hamburg;Harburg" als zwei separate Felder gelesen.
#
# Um dies zu verhindern, kann der entsprechende Wert in **Anführungszeichen** (oder ein anderes
# definiertes Zeichen) gesetzt werden. Das `csv`-Modul ignoriert dann Trennzeichen innerhalb
# dieser Anführungszeichen.
#
# Angenommener Inhalt der Datei 'datei2.csv' mit 'quoted' Feldern:
# Muenchen;1800000;MUC
# Berlin;3000000;BER
# Budapest;2000000;BUD
# Koeln;1500000;KLN
# "Hamburg;Harburg";800000;HAM  <-- Das Semikolon in "Hamburg;Harburg" wird ignoriert.

# Das `csv`-Modul erneut importieren (falls nicht bereits global geschehen)
import csv

# Öffnen der Datei 'datei2.csv'
with open('datei2.csv', newline='') as file2:
    # Erstellen eines `csv.reader`-Objekts mit definiertem 'quotechar'
    # Neben dem `delimiter` (hier ';') definieren wir `quotechar='"'`.
    # Das bedeutet, dass Zeichen innerhalb von doppelten Anführungszeichen als
    # ein einziges Feld behandelt werden, auch wenn sie den Delimiter enthalten.
    spamreader = csv.reader(file2, delimiter=';', quotechar='"')

    # Iterieren und Ausgabe der Zeilen
    for row in spamreader:
        # Die Felder der Zeile werden hier mit ", " anstatt als Liste ausgegeben,
        # um die Lesbarkeit des Ergebnisses zu verbessern.
        print(', '.join(row))

# Erwartete Ausgabe:
# Muenchen, 1800000, MUC
# Berlin, 3000000, BER
# Budapest, 2000000, BUD
# Koeln, 1500000, KLN
# Hamburg;Harburg, 800000,HAM