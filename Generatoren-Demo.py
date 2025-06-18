import time
import sys # Für die spätere optionale Speichernutzungs-Analyse

print("--- Performance-Vergleich: Liste vs. Generator (Zahlen von 0 bis 1.000.000.000) ---")

# --- Variante 1: Zahlen in einer Liste erzeugen ---
def generate_list_of_numbers(n):
    """
    Erzeugt und gibt eine Liste von Zahlen von 0 bis n-1 zurück.
    Alle Zahlen werden im Speicher gehalten.
    """
    numbers_list = []
    for i in range(n):
        numbers_list.append(i)
    return numbers_list

print("\nStarte Listen-Methode...")
start_time_list = time.perf_counter() # Misst die aktuelle Zeit mit hoher Präzision

# Die Funktion aufrufen, um die Liste zu erzeugen und zu befüllen
# Wir speichern die Liste, um den vollen Prozess zu simulieren
my_numbers_list = generate_list_of_numbers(1_000_000_000)

end_time_list = time.perf_counter() # Misst die Endzeit
elapsed_time_list = end_time_list - start_time_list
print(f"Listen-Methode abgeschlossen in: {elapsed_time_list:.4f} Sekunden")

# Optional: Speichernutzung der Liste anzeigen (kann bei sehr großen Listen viel sein)
# print(f"Größe der Liste im Speicher: {sys.getsizeof(my_numbers_list) / (1024 * 1024):.2f} MB")


# --- Variante 2: Zahlen mit einem Generator erzeugen ---
def generate_numbers_with_generator(n):
    """
    Erzeugt Zahlen von 0 bis n-1 mittels eines Generators.
    Zahlen werden einzeln bei Bedarf 'ge-yielded' und nicht im Speicher gesammelt.
    """
    for i in range(n):
        yield i

print("\nStarte Generator-Methode...")
start_time_gen = time.perf_counter() # Misst die aktuelle Zeit

# Den Generator erzeugen. Die Zahlen werden erst hier durchlaufen und 'konsumiert'.
# Um die Zeit für die Generierung zu messen, müssen wir den Generator komplett iterieren.
for num in generate_numbers_with_generator(1_000_000_000):
    pass # Wir tun nichts mit den Zahlen, da keine Ausgabe gewünscht ist

end_time_gen = time.perf_counter() # Misst die Endzeit
elapsed_time_gen = end_time_gen - start_time_gen
print(f"Generator-Methode abgeschlossen in: {elapsed_time_gen:.4f} Sekunden")

# Optional: Speichernutzung eines Generator-Objekts (ist sehr gering)
# gen_obj = generate_numbers_with_generator(1_000_000)
# print(f"Größe des Generator-Objekts im Speicher: {sys.getsizeof(gen_obj):.2f} Bytes")


print("\n--- Vergleich abgeschlossen ---")
if elapsed_time_list < elapsed_time_gen:
    print("Die Listen-Methode war in diesem Fall geringfügig schneller.")
else:
    print("Die Generator-Methode war in diesem Fall geringfügig schneller oder gleich schnell.")
print("Hinweis: Bei dieser Art von einfacher Zahlengenerierung ohne komplexe I/O-Operationen")
print("oder aufwendige Datenverarbeitung kann der Unterschied gering sein.")
print("Die Vorteile des Generators werden bei sehr großen Datenmengen, komplexen Objekten")
print("und/oder der Möglichkeit zum frühzeitigen Abbruch (wie im Crawler-Beispiel) deutlicher.")