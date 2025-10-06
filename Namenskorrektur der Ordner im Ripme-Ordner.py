import os
import sys
from fuzzywuzzy import fuzz

# --- Konfiguration ---
ZIEL_PFAD = r"e:\Bilder\Celebrities"
QUELLE_PFAD = r"d:\extracted\rips\reddit_sub_GermanCelebs"
SCHWELLENWERT = 75


# --- Ende Konfiguration ---

def sammle_zielnamen(pfad):
    """Sammelt ALLE Namen der Unterordner im Zielpfad, REKURSIV."""
    print(f"Lese korrekte Zielnamen (rekursiv) aus: {pfad}")
    korrekte_namen = {}
    try:
        for root, dirs, files in os.walk(pfad):
            if root == pfad:
                continue

            for d in dirs:
                if len(d) > 1:
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
        if beste_uebereinstimmung < 100:
            for ziel_name_lower in korrekte_namen_lower:
                score = fuzz.token_sort_ratio(falsch_name.lower(), ziel_name_lower)

                if score > beste_uebereinstimmung:
                    beste_uebereinstimmung = score
                    bester_zielname_korrekt = ziel_namen_map[ziel_name_lower]

        # 3. Vorschlag und Ausführung, wenn der Schwellenwert erreicht ist
        if bester_zielname_korrekt and beste_uebereinstimmung >= SCHWELLENWERT:

            # Überspringen, wenn der Name bereits exakt stimmt (vermeidet unnötige Fragen)
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
                    if beste_uebereinstimmung == 100:
                        # NEUE LOGIK: Zweischritt-Umbenennung für Casing-Korrektur
                        temp_name = falsch_name + "_TEMP_RENAME"
                        temp_pfad_voll = os.path.join(quelle_pfad, temp_name)

                        os.rename(quell_pfad_voll, temp_pfad_voll)
                        os.rename(temp_pfad_voll, ziel_pfad_voll)

                        print(
                            f"-> ERFOLGREICH (Zweischritt-Casing-Korrektur) umbenannt zu: '{bester_zielname_korrekt}'")
                        korrektur_zaehler += 1
                    else:
                        # Normale Fuzzy-Treffer (< 100%): Sicherstellen, dass das Ziel nicht schon existiert
                        if os.path.exists(ziel_pfad_voll):
                            print(
                                f"ACHTUNG: Zielordner '{bester_zielname_korrekt}' existiert bereits. Überspringe Umbenennung.")
                        else:
                            os.rename(quell_pfad_voll, ziel_pfad_voll)
                            print(f"-> ERFOLGREICH umbenannt zu: '{bester_zielname_korrekt}'")
                            korrektur_zaehler += 1

                except Exception as e:
                    print(f"FEHLER beim Umbenennen von '{falsch_name}': {e}")
            elif antwort == 's':
                print("-> Korrektur übersprungen.")
            else:
                print("-> Korrektur abgelehnt.")

    print(f"\n--- ZUSAMMENFASSUNG ---")
    print(f"{korrektur_zaehler} Ordner wurden erfolgreich umbenannt.")
    print("Nicht-korrigierte Ordner müssen manuell geprüft werden.")


# --- Hauptfunktion ---
if __name__ == "__main__":
    korrekte_namen_map = sammle_zielnamen(ZIEL_PFAD)

    if korrekte_namen_map:
        korrigiere_ordnernamen(korrekte_namen_map, QUELLE_PFAD)