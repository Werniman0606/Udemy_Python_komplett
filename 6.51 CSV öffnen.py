# In dieser Lektion wollen wir lernen, wie wir eine CSV-Datei öffnen
with open("datei.csv") as file:  # Datei wird geöffnet. Wir verwenden with,damit sie sich nach Nutzung automatisch schließt
    for line in file:  # für jede Zeile in dieser Datei
        print(line)  # gib den Inhalt aus
        # Ausgabe:
        # Muenchen;1800000;MUC
        # Berlin,3000000;BER
        # Budapest,2000000;BUD
        # Koeln;1500000;KLN

# Wenn wir den Inhalt der Datei von überflüssigen Leerzeichen bereinigen und an bestimmten Stellen zerteilen wollen, können wir das
# ebenfalls erreichen
with open("datei.csv") as file:  # Datei wird geöffnet. Wir verwenden with,damit sie sich nach Nutzung automatisch schließt
    for line in file:  # für jede Zeile in dieser Datei
        print(line.strip().split(";"))  # gib den Inhalt aus, entferne Leerzeichen am Anfang und Ende und splitte am Semikolon
        # Ausgabe:
        # ['Muenchen', '1800000', 'MUC']
        # ['Berlin,3000000', 'BER']
        # ['Budapest,2000000', 'BUD']
        # ['Koeln', '1500000', 'KLN']

        # Wir können die Daten aber auch weiterverwenden, indem wir sie in eine Liste packen und dann z.B. bestimmte Daten ausgeben
        data = line.strip().split(";") # die Datei wird bereinigt und gesplittet und in eine Liste verpackt
        print(data[0]+": "+data[1])
        # Ausgabe:
        # ['Muenchen', '1800000', 'MUC']
        # Muenchen: 1800000
        # ['Berlin,3000000', 'BER']
        # Berlin,3000000: BER
        # ['Budapest,2000000', 'BUD']
        # Budapest,2000000: BUD
        # ['Koeln', '1500000', 'KLN']
        # Koeln: 1500000