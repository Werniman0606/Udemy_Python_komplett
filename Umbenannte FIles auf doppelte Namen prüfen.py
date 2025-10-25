import os
from fuzzywuzzy import fuzz # Installationsbefehl: pip install fuzzywuzzy python-Levenshtein
from collections import defaultdict

# Konfigurieren des zu durchsuchenden Ordners
ROOT_FOLDER = r"e:\Celebrities"

# Ähnlichkeitsschwelle (Score von 0 bis 100).
# Werte über 85 sind meistens Tippfehler.
SIMILARITY_THRESHOLD = 88


def extract_persons_from_filename(filename):
    """
    Extrahiert die durch Komma getrennten Personennamen aus dem Präfix
    '[Person1, Person2]_...' und gibt sie als Liste zurück.
    """
    if filename.startswith('['):
        try:
            # Finde das schließende eckige Klammer-Zeichen und den Unterstrich
            end_index = filename.index(']_')
            # Extrahiere den Inhalt zwischen '[' und ']'
            prefix_content = filename[1:end_index]

            # Teile die Namen an Kommas und bereinige Leerzeichen
            persons = [name.strip() for name in prefix_content.split(',')]
            return persons
        except ValueError:
            return []
    return []


def collect_unique_person_names():
    """
    Durchsucht alle Dateinamen im ROOT_FOLDER und sammelt alle
    einzelnen, eindeutigen Personennamen.
    """
    unique_names = set()
    print(f"Sammle eindeutige Personennamen aus Dateinamen in '{ROOT_FOLDER}'...")

    for dirpath, _, filenames in os.walk(ROOT_FOLDER):
        for filename in filenames:
            # Nur relevante Dateiendungen prüfen (kann angepasst werden)
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            persons = extract_persons_from_filename(filename)
            for person in persons:
                # Normalisiere den Namen (z.B. alles Kleinbuchstaben) für den Vergleich
                unique_names.add(person.lower())

    print(f"Gefundene eindeutige Namen: {len(unique_names)}")
    return sorted(list(unique_names))


def find_similar_names(names):
    """
    Vergleicht alle Namen miteinander und identifiziert ähnliche Paare
    mithilfe der fuzzywuzzy-Bibliothek.
    """
    similar_pairs = []
    n = len(names)

    print("\nBeginne mit dem paarweisen Vergleich der Namen...")

    # Nur die untere Hälfte der Matrix vergleichen, da (A, B) = (B, A)
    for i in range(n):
        for j in range(i + 1, n):
            name1 = names[i]
            name2 = names[j]

            # Verwendet die Jaro-Winkler-Distanz (oder ähnliches)
            score = fuzz.ratio(name1, name2)

            if score >= SIMILARITY_THRESHOLD:
                # Wenn wir die normalisierten (kleingeschriebenen) Namen verglichen haben,
                # müssen wir die ursprüngliche Schreibweise finden.
                # Achtung: Da wir hier nur die kleingeschriebenen Namen haben,
                # geben wir diese aus und verlassen uns auf den Benutzer, die Groß-/Kleinschreibung zu korrigieren.
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
        print("-" * 50)
        print(f"Ergebnisse (Ähnlichkeit > {SIMILARITY_THRESHOLD}/100):")
        print("-" * 50)

        if not similar_pairs:
            print("Keine ähnlichen Namenspaare gefunden.")
            return

        # Ausgabe der Paare, gruppiert nach möglichen Korrekturen
        # Wir wählen immer den kürzeren/lexikographisch kleineren als den vermuteten "falschen" Namen
        for pair in sorted(similar_pairs, key=lambda x: x['score'], reverse=True):
            print(f"-> Score: {pair['score']} - {pair['name1']} <-> {pair['name2']}")

        print("-" * 50)
        print("Aktion erforderlich: Bitte überprüfen Sie diese Paare in Digikam und korrigieren Sie die Tags.")

    except ImportError:
        print("\n--- FEHLER: Bibliothek 'fuzzywuzzy' fehlt ---")
        print("Bitte installieren Sie die benötigte Bibliothek mit:")
        print("pip install fuzzywuzzy python-Levenshtein")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    main()