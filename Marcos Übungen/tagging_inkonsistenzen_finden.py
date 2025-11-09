# ==============================================================================
# Dateiname Vorschlag (Deutsch): tagging_inkonsistenzen_finden.py
# Dateiname Vorschlag (Technisch): fuzzy_tag_inconsistency_finder.py
#
# Beschreibung: Dieses Skript dient der Qualitätssicherung von Dateinamen-Tags.
#               1. Es liest rekursiv alle Personennamen (durch Komma getrennt)
#                  aus dem eckigen Klammer-Präfix der Dateinamen (z.B.
#                  '[Person A, Person B]_Datei.jpg').
#               2. Es normalisiert die Namen (alles Kleinbuchstaben).
#               3. Es verwendet Fuzzy Matching (Levenshtein-Distanz), um Paare
#                  von Namen zu identifizieren, die über einem definierten
#                  Ähnlichkeitsschwellenwert (SIMILARITY_THRESHOLD) liegen.
#               4. Ziel ist es, Tippfehler (z.B. 'Anna' vs. 'Annan') zu finden,
#                  die manuell in der Tag-Datenbank korrigiert werden müssen.
# ==============================================================================

import os
from fuzzywuzzy import fuzz # Installationsbefehl: pip install fuzzywuzzy python-Levenshtein
from collections import defaultdict

# --- Konfiguration ---
# Das Basisverzeichnis, in dem die Dateien mit den [TAG]_Präfixen liegen
ROOT_FOLDER = r"e:\Bilder\Celebrities"

# Ähnlichkeitsschwelle (Score von 0 bis 100).
# Werte über 85 deuten stark auf Tippfehler, Casing-Fehler oder kleine Abweichungen hin.
SIMILARITY_THRESHOLD = 88
# --- Ende Konfiguration ---


def extract_persons_from_filename(filename):
    """
    Extrahiert die durch Komma getrennten Personennamen aus dem Präfix
    '[Person1, Person2]_...' und gibt sie als Liste zurück.
    """
    if filename.startswith('['):
        try:
            # Findet das schließende eckige Klammer-Zeichen und den Unterstrich
            end_index = filename.index(']_')
            # Extrahiert den Inhalt zwischen '[' und ']_'
            prefix_content = filename[1:end_index]

            # Teilt die Namen an Kommas und bereinigt Leerzeichen
            persons = [name.strip() for name in prefix_content.split(',')]
            return persons
        except ValueError:
            # Falls die Struktur [Name] nicht gefunden wird (z.B. nur '[')
            return []
    return []


def collect_unique_person_names():
    """
    Durchsucht alle Dateinamen im ROOT_FOLDER und sammelt alle
    einzelnen, eindeutigen Personennamen, normalisiert in Kleinbuchstaben.
    """
    unique_names = set()
    print(f"Sammle eindeutige Personennamen aus Dateinamen in '{ROOT_FOLDER}'...")

    for dirpath, _, filenames in os.walk(ROOT_FOLDER):
        for filename in filenames:
            # Nur relevante Dateiendungen prüfen (kann angepasst werden)
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.tif')):
                continue

            persons = extract_persons_from_filename(filename)
            for person in persons:
                # Normalisiere den Namen (alles Kleinbuchstaben) für den Vergleich
                if person:
                    unique_names.add(person.lower())

    print(f"Gefundene eindeutige Namen (nach Normalisierung): {len(unique_names)}")
    return sorted(list(unique_names))


def find_similar_names(names):
    """
    Vergleicht alle Namen miteinander und identifiziert ähnliche Paare
    mithilfe der fuzzywuzzy-Bibliothek.
    """
    similar_pairs = []
    n = len(names)

    print(f"\nBeginne mit dem paarweisen Vergleich von {n} Namen...")

    # Nur die untere Hälfte der Matrix vergleichen, da (A, B) = (B, A)
    for i in range(n):
        for j in range(i + 1, n):
            name1 = names[i]
            name2 = names[j]

            # Verwendet fuzz.ratio, das die Levenshtein-Distanz verwendet
            score = fuzz.ratio(name1, name2)

            if score >= SIMILARITY_THRESHOLD:
                similar_pairs.append({
                    'name1': name1,
                    'name2': name2,
                    'score': score
                })

    return similar_pairs


def main():
    """
    Hauptfunktion zur Erkennung ähnlicher Namen.
    """
    try:
        # 1. Namen sammeln
        names = collect_unique_person_names()

        if not names:
            print("Keine Personennamen-Präfixe in den Dateinamen gefunden. Beende.")
            return

        # 2. Ähnliche Paare finden
        similar_pairs = find_similar_names(names)

        # 3. Ergebnis ausgeben
        print("\n" + "=" * 50)
        print(f"Ergebnisse (Ähnlichkeit > {SIMILARITY_THRESHOLD}/100):")
        print("=" * 50)

        if not similar_pairs:
            print("Keine ähnlichen Namenspaare gefunden. Ihre Tags sind konsistent! 🎉")
            return

        # Ausgabe der Paare, sortiert nach absteigender Ähnlichkeit (die wahrscheinlichsten Fehler zuerst)
        # Die Namen sind in Kleinbuchstaben, um Casing-Fehler zu ignorieren.
        for pair in sorted(similar_pairs, key=lambda x: x['score'], reverse=True):
            print(f"-> Score: **{pair['score']}** - '{pair['name1']}' <-> '{pair['name2']}'")

        print("=" * 50)
        print("💡 **Aktion erforderlich:** Bitte überprüfen Sie diese Paare.")
        print("Wahrscheinlich handelt es sich um Tippfehler (z.B. 'Anna' vs. 'Annan') oder unterschiedliche Schreibweisen.")

    except ImportError:
        print("\n--- ❌ FEHLER: Bibliothek 'fuzzywuzzy' fehlt ---")
        print("Bitte installieren Sie die benötigte Bibliothek mit:")
        print("**pip install fuzzywuzzy python-Levenshtein**")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    main()