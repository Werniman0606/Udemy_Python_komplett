# ==============================================================================
# Dateiname Vorschlag (Deutsch): dateiname_tag_haeufigkeit_zaehlen.py
# Dateiname Vorschlag (Technisch): filename_tag_frequency_counter.py
#
# Beschreibung: Dieses Skript analysiert rekursiv (oder in diesem Fall, nur den
#               obersten Ordner) alle JPG-Dateien in einem angegebenen Pfad.
#               Es extrahiert den Personennamen, der in eckigen Klammern am
#               Anfang des Dateinamens steht (z.B. '[Amy Lee]_Foto.jpg').
#               Anschließend zählt und listet es alle gefundenen eindeutigen
#               Namen auf, sortiert nach deren Häufigkeit (die Anzahl der Dateien).
#               Dies dient dazu, die Tag-Verteilung der Sammlung zu ermitteln.
# ==============================================================================

import os
import re
from collections import Counter

# 1. Definieren des Ordnerpfades und des Regex
ORDNERPFAD = r"d:\Celebs"  # Der Pfad zum Ordner
# Regex-Muster: Sucht nach Zeichen ([^\]]+) innerhalb der ersten eckigen Klammern (\[...\])
# Das Fragezeichen macht es "non-greedy" und sucht nur nach dem ersten Vorkommen
NAMEN_REGEX = r"\[([^\]]+?)\]"

# Liste zur Speicherung aller gefundenen Personennamen
gefundene_namen = []

# 2. Durchlaufen der Dateien im Ordner
print(f"Starte Analyse der Dateinamen in: {ORDNERPFAD}\n")
try:
    # Nur der oberste Ordner wird durchsucht
    for dateiname in os.listdir(ORDNERPFAD):
        # Wir sind nur an regulären Dateien mit der erwarteten Endung interessiert
        if os.path.isfile(os.path.join(ORDNERPFAD, dateiname)) and dateiname.lower().endswith(".jpg"):

            # Führe den Regex-Match durch
            match = re.search(NAMEN_REGEX, dateiname)

            if match:
                # Die erste erfasste Gruppe (der Inhalt der Klammern) ist der Personenname
                personenname = match.group(1).strip()  # .strip() entfernt Leerzeichen am Anfang/Ende
                gefundene_namen.append(personenname)

# Fehlerbehandlung, falls der Pfad nicht existiert oder keine Berechtigung besteht
except FileNotFoundError:
    print(f"Fehler: Der angegebene Ordnerpfad '{ORDNERPFAD}' wurde nicht gefunden.")
    exit()
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    exit()

# 3. Zählen und Sortieren der Namen
if gefundene_namen:
    # Zählt die Häufigkeit jedes Namens
    namens_zaehler = Counter(gefundene_namen)

    # Sortiert die Ergebnisse in absteigender Reihenfolge der Häufigkeit
    # key=lambda item: item[1] sortiert nach dem zweiten Element des Tupels (der Zählung)
    sortierte_namen = sorted(namens_zaehler.items(), key=lambda item: item[1], reverse=True)

    # 4. Ausgabe der Ergebnisse
    print(f"✅ Analyse abgeschlossen für Ordner: {ORDNERPFAD}\n")
    print("=" * 50)
    print("--- Häufigkeit der Personennamen (Absteigend) ---")
    print("=" * 50)

    for name, anzahl in sortierte_namen:
        # Die Ausgabe zeigt, wie oft ein bestimmter Name als Präfix verwendet wurde
        print(f"Name: **{name}** - Vorkommen: **{anzahl}**")

    print("=" * 50)

else:
    print(f"❌ Keine Dateien mit der Endung '.jpg' und der Namensstruktur '[Name]...' im Ordner '{ORDNERPFAD}' gefunden.")