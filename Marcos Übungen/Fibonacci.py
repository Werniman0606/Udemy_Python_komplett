def fibonacci_reihe(n): # eine neue Methode wird angelegt
    """
    Diese Funktion gibt die ersten n Zahlen der Fibonacci-Reihe aus.

    Die Fibonacci-Reihe beginnt mit 0 und 1. Jede weitere Zahl ist die Summe der beiden
    vorhergehenden Zahlen (z.B. 0, 1, 1, 2, 3, 5, 8, ...).

    Args:
        n (int): Die Anzahl der auszugebenden Fibonacci-Zahlen.
                 Muss eine nicht-negative Ganzzahl sein.

    Returns:
        list: Eine Liste der ersten n Fibonacci-Zahlen.
              Gibt eine leere Liste zurück, wenn n 0 ist.
              Gibt [0] zurück, wenn n 1 ist.
    """
    if n < 0:
        # Negative Eingaben sind ungültig; Fehlermeldung ausgeben und leere Liste zurückgeben.
        print("Bitte geben Sie eine nicht-negative Zahl ein.")
        return []
    elif n == 0:
        # Für n=0 gibt es keine Fibonacci-Zahlen, daher eine leere Liste.
        return []
    elif n == 1:
        # Basisfall: Die erste Fibonacci-Zahl ist 0.
        return [0]
    else:
        # Initialisiere die Reihe mit den ersten beiden Fibonacci-Zahlen.
        reihe = [0, 1]
        # Füge weitere Zahlen hinzu, bis die gewünschte Länge 'n' erreicht ist.
        while len(reihe) < n:
            # Die nächste Fibonacci-Zahl ist die Summe der beiden vorhergehenden.
            next_fib = reihe[-1] + reihe[-2]
            reihe.append(next_fib)
        return reihe

# Beispiel-Aufrufe der Funktion:
print(f"Die ersten 0 Fibonacci-Zahlen: {fibonacci_reihe(0)}") # die Methode wird mit dem Parameter 0 gestartet
print(f"Die ersten 1 Fibonacci-Zahlen: {fibonacci_reihe(1)}")
print(f"Die ersten 5 Fibonacci-Zahlen: {fibonacci_reihe(5)}")
print(f"Die ersten 10 Fibonacci-Zahlen: {fibonacci_reihe(10)}")
print(f"Die ersten 20 Fibonacci-Zahlen: {fibonacci_reihe(20)}")

# Benutzerinteraktion (optional):
# try:
#     num_elements = int(input("Wie viele Fibonacci-Zahlen möchten Sie sehen? "))
#     fib_zahlen = fibonacci_reihe(num_elements)
#     if fib_zahlen:
#         print(f"Die ersten {num_elements} Fibonacci-Zahlen sind: {fib_zahlen}")
# except ValueError:
#     print("Ungültige Eingabe. Bitte geben Sie eine ganze Zahl ein.")

"""
So funktioniert das Programm

Dieses Python-Programm enthält eine Funktion namens fibonacci_reihe(n), die die ersten n Zahlen der Fibonacci-Reihe generiert.

    Funktionsdefinition (fibonacci_reihe(n)):

        Sie nimmt einen Parameter n entgegen, der angibt, wie viele Fibonacci-Zahlen ausgegeben werden sollen.

        Fehlerbehandlung: Es wird geprüft, ob n negativ ist, und eine entsprechende Meldung ausgegeben.

        Basisfälle:

            Wenn n 0 ist, wird eine leere Liste zurückgegeben.

            Wenn n 1 ist, wird eine Liste mit der ersten Fibonacci-Zahl [0] zurückgegeben.

        Hauptlogik:

            Für n größer als 1 wird eine Liste reihe mit den ersten beiden Fibonacci-Zahlen [0, 1] initialisiert.

            Eine while-Schleife läuft, solange die Länge der Liste kleiner als n ist.

            In jedem Schleifendurchlauf wird die nächste Fibonacci-Zahl berechnet, indem die letzten beiden Zahlen in der Liste addiert werden (reihe[-1] + reihe[-2]).

            Die berechnete Zahl wird dann der Liste hinzugefügt (reihe.append(next_fib)).

            Sobald die Liste n Zahlen enthält, wird sie zurückgegeben.

    Beispiel-Aufrufe:

        Am Ende des Codes siehst du mehrere print-Anweisungen, die die Funktion mit verschiedenen Werten für n aufrufen und die Ergebnisse anzeigen.

    Benutzerinteraktion (optional):

        Der auskommentierte Abschnitt zeigt, wie du das Programm interaktiver gestalten könntest, indem du den Benutzer nach der Anzahl der gewünschten Fibonacci-Zahlen fragst. Du kannst die Rautezeichen (#) entfernen, um diesen Teil zu aktivieren.

Diese Implementierung ist eine klassische und effiziente Methode, um die Fibonacci-Reihe iterativ zu erzeugen.

"""
