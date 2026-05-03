# ==============================================================================
# Dateiname: folder_name_fuzzy_corrector_v2.py
#
# Beschreibung: Standardisiert Ordnernamen basierend auf einem Archiv.
#               - Korrigiert Tippfehler (Fuzzy Matching)
#               - Korrigiert Groß-/Kleinschreibung (Windows NTFS Fix)
#               - NEU: Mergt Ordner, falls der Zielname bereits existiert.
# ==============================================================================

import os
import sys
import shutil
from fuzzywuzzy import fuzz  # Benötigt: pip install fuzzywuzzy python-levenshtein

# --- Konfiguration ---
ZIEL_PFAD = r"e:\Bilder\Celebrities"
QUELLE_PFAD = r"d:\extracted\rips\reddit_sub_GermanCelebs"
SCHWELLENWERT = 75


def sammle_zielnamen(pfad):
    """Sammelt ALLE Namen der Unterordner im Zielpfad, REKURSIV."""
    print(f"Lese korrekte Zielnamen (rekursiv) aus: {pfad}")
    korrekte_namen = {}
    try:
        for root, dirs, files in os.walk(pfad):
            for d in dirs:
                if len(d) > 1:
                    korrekte_namen[d.lower()] = d
        print(f"-> {len(korrekte_namen)} korrekte Namen zur Prüfung gefunden.")
        return korrekte_namen
    except Exception as e:
        print(f"FEHLER beim Lesen des Zielpfads: {e}")
        sys.exit(1)


def merge_ordner(quell_ordner_pfad, ziel_ordner_pfad):
    """Verschiebt den Inhalt von Quelle in Ziel und löscht die leere Quelle."""
    try:
        for item in os.listdir(quell_ordner_pfad):
            s = os.path.join(quell_ordner_pfad, item)
            d = os.path.join(ziel_ordner_pfad, item)

            # Falls Datei/Ordner im Ziel existiert, Suffix anhängen um Überschreiben zu verhindern
            if os.path.exists(d):
                base, extension = os.path.splitext(item)
                d = os.path.join(ziel_ordner_pfad, f"{base}_DUPLIKAT{extension}")

            shutil.move(s, d)

        # Leeren Quellordner entfernen
        os.rmdir(quell_ordner_pfad)
        return True
    except Exception as e:
        print(f"   ❌ Fehler beim Mergen: {e}")
        return False


def korrigiere_ordnernamen(ziel_namen_map, quelle_pfad):
    """Durchsucht den Quellpfad und schlägt Korrekturen oder Merges vor."""
    print(f"\nStarte Überprüfung in: {quelle_pfad}")
    korrekte_namen_lower = ziel_namen_map.keys()

    try:
        quell_ordner = [d for d in os.listdir(quelle_pfad) if os.path.isdir(os.path.join(quelle_pfad, d))]
    except FileNotFoundError:
        print(f"FEHLER: Quellpfad '{quelle_pfad}' nicht gefunden.")
        return

    korrektur_zaehler = 0

    for falsch_name in quell_ordner:
        beste_uebereinstimmung = 0
        bester_zielname_korrekt = None

        # 1. Exakte Übereinstimmung (ohne Case)
        if falsch_name.lower() in ziel_namen_map:
            beste_uebereinstimmung = 100
            bester_zielname_korrekt = ziel_namen_map[falsch_name.lower()]

        # 2. Fuzzy Matching
        if beste_uebereinstimmung < 100:
            for ziel_name_lower in korrekte_namen_lower:
                score = fuzz.token_sort_ratio(falsch_name.lower(), ziel_name_lower)
                if score > beste_uebereinstimmung:
                    beste_uebereinstimmung = score
                    bester_zielname_korrekt = ziel_namen_map[ziel_name_lower]

        # 3. Ausführung
        if bester_zielname_korrekt and beste_uebereinstimmung >= SCHWELLENWERT:
            if falsch_name == bester_zielname_korrekt:
                continue

            quell_pfad_voll = os.path.join(quelle_pfad, falsch_name)
            ziel_pfad_voll = os.path.join(quelle_pfad, bester_zielname_korrekt)

            print(f"\n--- AKTION VORGESCHLAGEN ({beste_uebereinstimmung}%) ---")
            print(f"Quelle: '{falsch_name}'")
            print(f"Ziel:   '{bester_zielname_korrekt}'")

            status = "MERGE" if os.path.exists(
                ziel_pfad_voll) and falsch_name.lower() != bester_zielname_korrekt.lower() else "RENAME"
            print(f"Modus:  {status}")

            antwort = input(f"Zustimmen? (j/n/s): ").lower()

            if antwort == 'j':
                try:
                    # FALL: Zielordner existiert -> MERGEN
                    if os.path.exists(ziel_pfad_voll) and quell_pfad_voll.lower() != ziel_pfad_voll.lower():
                        if merge_ordner(quell_pfad_voll, ziel_pfad_voll):
                            print(f"-> Erfolgreich zusammengeführt.")
                            korrektur_zaehler += 1

                    # FALL: Nur Groß-/Kleinschreibung falsch (NTFS-Safe Rename)
                    elif beste_uebereinstimmung == 100:
                        temp_pfad = quell_pfad_voll + "_TEMP"
                        os.rename(quell_pfad_voll, temp_pfad)
                        os.rename(temp_pfad, ziel_pfad_voll)
                        print(f"-> Schreibweise korrigiert.")
                        korrektur_zaehler += 1

                    # FALL: Normales Umbenennen
                    else:
                        os.rename(quell_pfad_voll, ziel_pfad_voll)
                        print(f"-> Ordner umbenannt.")
                        korrektur_zaehler += 1

                except Exception as e:
                    print(f"❌ Fehler: {e}")

    print(f"\n--- FERTIG: {korrektur_zaehler} Korrekturen durchgeführt. ---")


def main():
    ziel_namen_map = sammle_zielnamen(ZIEL_PFAD)
    if ziel_namen_map:
        korrigiere_ordnernamen(ziel_namen_map, QUELLE_PFAD)


if __name__ == "__main__":
    main()