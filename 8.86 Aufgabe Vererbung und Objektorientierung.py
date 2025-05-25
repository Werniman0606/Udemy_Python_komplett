# --- Lektion: Dateiverarbeitung mit Vererbung (FileReader und CsvReader) ---

# In dieser Lektion lernen wir ein praktisches Beispiel kennen, das zeigt,
# wie Daten mit Objektorientierung verarbeitet werden können und wie Vererbung funktioniert.
# Wir erstellen zwei Klassen: eine allgemeine für das Lesen von Dateien und eine spezialisierte
# für das Lesen von CSV-Dateien.

# --- Aufgabe 1: Die Basisklasse - FileReader ---
# Vervollständige die Klasse Filereader so, dass bei Aufruf der lines()-Methode die Datei Zeile für Zeile
# eingelesen wird. Die lines-Methode soll eine Liste der Zeilen in der Datei zurückgeben.

# --- Aufgabe 2: Die spezialisierte Klasse - CsvReader ---
# Erstelle die Klasse Csv-Reader so dass der FileReader erweitert wird. Bei Aufruf der lines() soll die
# Datei als *.csv-Datei eingelesen werden, d.h. es soll eine mehrdimensionale Liste zurückgegeben werden.

class FileReader():
    # Der Konstruktor: Diese spezielle Funktion wird immer ausgeführt, wenn du eine neue Instanz (ein Objekt)
    # der Klasse FileReader erstellst. Sie dient dazu, das Objekt zu initialisieren.
    def __init__(self, filename):
        # Der übergebene Dateiname (filename) wird als Instanzvariable 'self.filename' gespeichert.
        # So kann jedes Objekt dieser Klasse wissen, welche Datei es bearbeiten soll.
        self.filename = filename

    # Die 'lines'-Methode: Diese Methode ist dafür verantwortlich, den Inhalt der Datei
    # zeilenweise einzulesen.
    def lines(self):
        lines = []  # Eine leere Liste namens 'lines' wird erzeugt. Hier werden die einzelnen Zeilen gesammelt.

        # Die Datei, deren Pfad in 'self.filename' gespeichert ist, wird zum Lesen ("r") geöffnet.
        # Die 'with'-Anweisung sorgt dafür, dass die Datei automatisch und sicher geschlossen wird,
        # auch wenn ein Fehler auftritt.
        with open(self.filename, "r") as file:
            # Eine Schleife geht jede 'line' in der geöffneten 'file' durch.
            for line in file:
                # Jede gelesene 'line' wird zur Liste 'lines' hinzugefügt.
                # '.strip()' entfernt dabei alle führenden und nachfolgenden Leerzeichen sowie
                # Zeilenumbruchzeichen (wie '\n') von der Zeile.
                lines.append(line.strip())
        # Nach dem Einlesen aller Zeilen wird die vollständige Liste 'lines' zurückgegeben.
        return lines


class CsvReader(FileReader):  # Die Klasse CsvReader erbt von der Klasse FileReader.
    # Das bedeutet, CsvReader übernimmt automatisch alle Funktionen und Eigenschaften
    # von FileReader und kann diese bei Bedarf erweitern oder ändern.

    # Der Konstruktor von CsvReader: Wird aufgerufen, wenn ein neues CsvReader-Objekt erstellt wird.
    def __init__(self, filename):
        # 'super().__init__(filename)' ruft den Konstruktor der direkten Elternklasse (FileReader) auf.
        # Dadurch wird der Dateiname korrekt in 'self.filename' initialisiert, wie es in FileReader definiert ist.
        super().__init__(filename)

    # Die 'lines'-Methode wird hier überschrieben (dies nennt man Method Overriding).
    # Sie hat denselben Namen wie die Methode in FileReader, aber eine spezielle Implementierung
    # für das Lesen von CSV-Dateien.
    def lines(self):
        # Zuerst ruft 'super().lines()' die 'lines()'-Methode der Elternklasse (FileReader) auf.
        # Dies liefert uns eine Liste von Strings, wobei jeder String eine Zeile der CSV-Datei ist,
        # aber noch nicht in Spalten aufgeteilt (z.B. ['Name,Vorname', 'Jahn,Marco']).
        lines = super().lines()

        lines_splittet = []  # Eine neue, leere Liste namens 'lines_splittet' wird erzeugt.
        # Hier werden die gesplitteten Zeilen als Unterlisten gespeichert.

        # Die Schleife durchläuft jeden 'line'-String aus der von der Elternklasse erhaltenen Liste.
        for line in lines:
            # Jeder 'line'-String wird am Komma (",") gesplittet. Dies erzeugt eine Liste von Strings
            # für die aktuelle Zeile (z.B. ['Jahn', 'Marco']).
            # Diese Liste (die die aufgeteilten Spalten darstellt) wird dann an 'lines_splittet' angehängt.
            lines_splittet.append(line.split(","))

        # Nachdem alle Zeilen verarbeitet wurden, wird die "mehrdimensionale Liste" 'lines_splittet'
        # zurückgegeben. Jedes Element in dieser Liste ist eine weitere Liste, die die Spalten einer Zeile enthält.
        return lines_splittet
        # man könnte die Zeilen 62-74 auch vermeiden, indem man direkt eine Liste zurückgibt:
        # return [line.split(",") for line in lines]
        # Das nennt man List comprehension


# --- Tests der Klassenfunktionalität ---

# Test der FileReader-Klasse:
# Erstellt ein neues Objekt 'f' vom Typ FileReader. Der Dateiname wird als Argument übergeben.
f = FileReader("./datei.csv")  # Beachte: Hier wird der Dateiname 'datei.csv' verwendet.

print("Ausgabe von FileReader.lines():")
# Ruft die 'lines()'-Methode des 'f'-Objekts auf und gibt deren Rückgabe aus.
print(f.lines())
# Erwartete Ausgabe:
# ['Nachname,Vorname', 'Mustermann,Max', 'Müller,Monika']
# (Gibt jede Zeile als einen String zurück, wie sie in der Datei steht, aber ohne Zeilenumbruchzeichen.)


print("\n" + "=" * 30 + "\n")  # Eine Trennlinie zur besseren Unterscheidung der Ausgaben.

# Test der CsvReader-Klasse:
# Erstellt ein neues Objekt 'f' vom Typ CsvReader. Auch hier wird der Dateiname übergeben.
f = CsvReader("./datei.csv")  # Beachte: Hier wird der Dateiname 'datei.csv' verwendet.

print("Ausgabe von CsvReader.lines():")
# Ruft die 'lines()'-Methode des 'f'-Objekts auf und gibt deren Rückgabe aus.
print(f.lines())
# Erwartete Ausgabe:
# [['Nachname', 'Vorname'], ['Mustermann', 'Max'], ['Müller', 'Monika']]
# (Gibt eine Liste von Listen zurück, wobei jede innere Liste die einzelnen Werte einer CSV-Zeile darstellt.)

# Deine tatsächliche Ausgabe:
# [['Name', 'Vorname'], ['Jahn', 'Marco'], ['Jahn', 'Sandra'], ...]
# Diese Ausgabe ist korrekt für eine CSV-Datei mit den von dir genannten Familienmitgliedern.
