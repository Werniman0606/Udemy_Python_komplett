# ==============================================================================
# Dateiname Vorschlag (Deutsch): ordnernamen_fuzzy_korrigieren.py
# Dateiname Vorschlag (Technisch): folder_name_fuzzy_corrector.py
#
# Beschreibung: Dieses Skript dient der Standardisierung und Korrektur von
#               Ordnernamen (z.B. in einem Download-Ordner) anhand einer
#               bestehenden, korrekten Ordnerstruktur (dem Archiv).
#               1. Es liest alle korrekten Ordnernamen aus ZIEL_PFAD (rekursiv) ein.
#               2. Es durchsucht die oberste Ebene des QUELLE_PFAD nach Abweichungen.
#               3. Es verwendet Fuzzy Matching (fuzz.token_sort_ratio) und einen
#                  Schwellenwert (SCHWELLENWERT), um Tippfehler zu erkennen und
#                  den korrekten Namen vorzuschlagen.
#               4. Bei 100% Übereinstimmung (ohne Berücksichtigung der Groß-/
#                  Kleinschreibung) wird eine Zweischritt-Umbenennung durchgeführt,
#                  um nur das korrekte Casing des Namens zu erzwingen.
#               5. Der Benutzer muss jede Umbenennung manuell bestätigen.
# ==============================================================================

import os
import sys
from fuzzywuzzy import fuzz  # Benötigt: pip install fuzzywuzzy python-levenshtein

# --- Konfiguration ---
# Das Archiv/die Sammlung, aus der die KORREKTEN Ordnernamen gelesen werden (rekursiv)
ZIEL_PFAD = r"e:\Bilder\Celebrities"
# Der Ordner mit den zu prüfenden Ordnern (z.B. neue Downloads)
QUELLE_PFAD = r"d:\rips\reddit_sub_GermanCelebs"
# Ähnlichkeitsschwelle (0-100), ab der eine Korrektur vorgeschlagen wird
SCHWELLENWERT = 75


# --- Ende Konfiguration ---

def sammle_zielnamen(pfad):
    """Sammelt ALLE Namen der Unterordner im Zielpfad, REKURSIV."""
    print(f"Lese korrekte Zielnamen (rekursiv) aus: {pfad}")
    # Speichert: {kleingeschriebener_name: Name_mit_korrektem_Casing}
    korrekte_namen = {}
    try:
        # Durchläuft rekursiv alle Unterordner
        for root, dirs, files in os.walk(pfad):
            # Wir sind nur an den Namen interessiert, nicht an den Pfad-Bestandteilen
            for d in dirs:
                if len(d) > 1:  # Ignoriert möglicherweise "." oder kurze Platzhalter
                    # Speichert den kleingeschriebenen Namen als Schlüssel, den Originalnamen als Wert
                    korrekte_namen[d.lower()] = d

        print(f"-> {len(korrekte_namen)} korrekte Namen zur Prüfung gefunden.")
        return korrekte_namen

    except FileNotFoundError:
        print(f"FEHLER: Zielpfad '{pfad}' nicht gefunden. Bitte prüfen Sie die ZIEL_PFAD Variable.")
        sys.exit(1)
    except Exception as e:
        print(f"FEHLER beim Lesen des Zielpfads: {e}")
        sys.exit(1)


def korrigiere_ordnernamen(ziel_namen_map, quelle_pfad):
    """Durchsucht den Quellpfad, findet ähnliche Namen und schlägt Korrekturen vor."""
    print(f"\nStarte Überprüfung im Quellpfad: {quelle_pfad}")
    korrekte_namen_lower = ziel_namen_map.keys()

    try:
        # Nur Ordner in der obersten Ebene des Quellpfads prüfen
        quell_ordner = [d for d in os.listdir(quelle_pfad) if os.path.isdir(os.path.join(quelle_pfad, d))]
        print(f"-> {len(quell_ordner)} Quellordner zum Prüfen gefunden.")
    except FileNotFoundError:
        print(f"FEHLER: Quellpfad '{quelle_pfad}' nicht gefunden. Bitte prüfen Sie die QUELLE_PFAD Variable.")
        return

    korrektur_zaehler = 0

    for falsch_name in quell_ordner:
        beste_uebereinstimmung = 0
        bester_zielname_korrekt = None

        # 1. Prüfen auf exakte Übereinstimmung (ohne Casing)
        if falsch_name.lower() in ziel_namen_map:
            beste_uebereinstimmung = 100
            bester_zielname_korrekt = ziel_namen_map[falsch_name.lower()]

        # 2. Fuzzy Matching, falls keine perfekte Übereinstimmung gefunden wurde
        # (Dies fängt Tippfehler ab, aber nicht 100% Casing-Fehler)
        if beste_uebereinstimmung < 100:
            for ziel_name_lower in korrekte_namen_lower:
                # Nutzt Token Sort Ratio für robusten Vergleich
                score = fuzz.token_sort_ratio(falsch_name.lower(), ziel_name_lower)

                if score > beste_uebereinstimmung:
                    beste_uebereinstimmung = score
                    bester_zielname_korrekt = ziel_namen_map[ziel_name_lower]

        # 3. Vorschlag und Ausführung, wenn der Schwellenwert erreicht ist
        if bester_zielname_korrekt and beste_uebereinstimmung >= SCHWELLENWERT:

            # Wenn der Name bereits exakt stimmt (inkl. Casing), überspringen
            if falsch_name == bester_zielname_korrekt:
                continue

            quell_pfad_voll = os.path.join(quelle_pfad, falsch_name)
            ziel_pfad_voll = os.path.join(quelle_pfad, bester_zielname_korrekt)

            print(f"\n--- POTENZIELLE KORREKTUR VORGESCHLAGEN ---")
            print(f"Falscher Name:  '{falsch_name}'")
            print(f"Vorschlag:     '{bester_zielname_korrekt}' (Ähnlichkeit: {beste_uebereinstimmung}%)")

            antwort = input("Umbenennen? (j/n/s - 's' für springen): ").lower()

            if antwort == 'j':
                try:
                    if beste_uebereinstimmung == 100 and os.path.isdir(quell_pfad_voll) and not os.path.exists(
                            ziel_pfad_voll):
                        # NEUE LOGIK: Zweischritt-Umbenennung, um Casing-Korrektur auf NTFS zu erzwingen
                        # (Da Windows NTFS Case-Insensitive ist, kann man 'a' nicht direkt in 'A' umbenennen)
                        temp_name = falsch_name + "_TEMP_RENAME"
                        temp_pfad_voll = os.path.join(quelle_pfad, temp_name)

                        os.rename(quell_pfad_voll, temp_pfad_voll)
                        os.rename(temp_pfad_voll, ziel_pfad_voll)

                        print(f"-> ERFOLGREICH (Casing-Korrektur) umbenannt zu: '{bester_zielname_korrekt}'")
                        korrektur_zaehler += 1
                    else:
                        # Normale Fuzzy-Treffer (< 100%) oder andere Fälle
                        if os.path.exists(ziel_pfad_voll):
                            # KORREKTUR: Der f-String wird hier abgeschlossen
                            print(
                                f"ACHTUNG: Zielordner '{bester_zielname_korrekt}' existiert bereits. Umbenennung übersprungen.")
                        else:
                            # Normale Umbenennung
                            os.rename(quell_pfad_voll, ziel_pfad_voll)
                            print(f"-> ERFOLGREICH umbenannt zu: '{bester_zielname_korrekt}'")
                            korrektur_zaehler += 1

                except Exception as e:
                    print(f"❌ FEHLER beim Umbenennen von '{falsch_name}' zu '{bester_zielname_korrekt}': {e}")

            elif antwort == 's':
                print(f"-> Umbenennung von '{falsch_name}' übersprungen.")
            else:
                print("-> Aktion abgebrochen oder ungültige Eingabe.")

    print(f"\n--- ZUSAMMENFASSUNG ---")
    print(f"Insgesamt {len(quell_ordner)} Ordner geprüft.")
    print(f"Anzahl erfolgreicher Korrekturen: {korrektur_zaehler}")
    print("-" * 30)

# --- Hauptfunktion und Start ---

def main():
    """Startet den gesamten Prozess."""
    ziel_namen_map = sammle_zielnamen(ZIEL_PFAD)

    if ziel_namen_map:
        korrigiere_ordnernamen(ziel_namen_map, QUELLE_PFAD)


if __name__ == "__main__":
    main()