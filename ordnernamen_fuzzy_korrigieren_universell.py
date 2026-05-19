# ==============================================================================
# Dateiname: folder_name_fuzzy_corrector_v2.py
#
# Beschreibung: Standardisiert Ordnernamen basierend auf einem Archiv.
#                - Korrigiert Tippfehler (Fuzzy Matching)
#                - Korrigiert Groß-/Kleinschreibung (Windows NTFS Fix)
#                - Mergt Ordner, falls der Zielname bereits existiert.
#
# Funktioniert nativ unter Windows UND Linux (CachyOS).
# ==============================================================================

import os
import sys
import shutil
from pathlib import Path
from fuzzywuzzy import fuzz  # Benötigt: pip install fuzzywuzzy python-levenshtein

# --- KONFIGURATION & BETRIEBSSYSTEM-ERKENNUNG ---
if os.name == 'nt':  # Windows
    ZIEL_PFAD = Path(r"e:\Bilder\Celebrities")
    QUELLE_PFAD = Path(r"d:\extracted\rips\reddit_sub_GermanCelebs")
else:  # Linux (CachyOS)
    ZIEL_PFAD = Path("/run/media/marcoj/Laufwerk E/Bilder/Celebrities")
    QUELLE_PFAD = Path("/run/media/marcoj/Laufwerk D/extracted/rips/reddit_sub_GermanCelebs")

SCHWELLENWERT = 75


def sammle_zielnamen(pfad):
    """Sammelt ALLE Namen der Unterordner im Zielpfad, REKURSIV."""
    print(f"Lese korrekte Zielnamen (rekursiv) aus: {pfad}")
    korrekte_namen = {}
    try:
        # rglob('*') findet alles, wir filtern über .is_dir()
        for d in pfad.rglob('*'):
            if d.is_dir() and len(d.name) > 1:
                korrekte_namen[d.name.lower()] = d.name
        print(f"-> {len(korrekte_namen)} korrekte Namen zur Prüfung gefunden.")
        return korrekte_namen
    except Exception as e:
        print(f"FEHLER beim Lesen des Zielpfads: {e}")
        sys.exit(1)


def merge_ordner(quell_ordner_pfad, ziel_ordner_pfad):
    """Verschiebt den Inhalt von Quelle in Ziel und löscht die leere Quelle."""
    try:
        # .iterdir() listet alle Dateien/Ordner im Verzeichnis auf
        for item in quell_ordner_pfad.iterdir():
            s = item
            d = ziel_ordner_pfad / item.name

            # Falls Datei/Ordner im Ziel existiert, Suffix anhängen um Überschreiben zu verhindern
            if d.exists():
                # .stem ist der Name ohne Endung, .suffix ist die Endung mit Punkt
                d = ziel_ordner_pfad / f"{item.stem}_DUPLIKAT{item.suffix}"

            shutil.move(s, d)

        # Leeren Quellordner entfernen
        quell_ordner_pfad.rmdir()
        return True
    except Exception as e:
        print(f"    ❌ Fehler beim Mergen: {e}")
        return False


def korrigiere_ordnernamen(ziel_namen_map, quelle_pfad):
    """Durchsucht den Quellpfad und schlägt Korrekturen oder Merges vor."""
    print(f"\nStarte Überprüfung in: {quelle_pfad}")
    korrekte_namen_lower = ziel_namen_map.keys()

    if not quelle_pfad.is_dir():
        print(f"FEHLER: Quellpfad '{quelle_pfad}' nicht gefunden.")
        return

    # Holt nur die direkten Unterordner der ersten Ebene
    quell_ordner = [d for d in quelle_pfad.iterdir() if d.is_dir()]
    korrektur_zaehler = 0

    for quell_dir in quell_ordner:
        falsch_name = quell_dir.name
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

            quell_pfad_voll = quell_dir
            ziel_pfad_voll = quelle_pfad / bester_zielname_korrekt

            print(f"\n--- AKTION VORGESCHLAGEN ({beste_uebereinstimmung}%) ---")
            print(f"Quelle: '{falsch_name}'")
            print(f"Ziel:   '{bester_zielname_korrekt}'")

            status = "MERGE" if ziel_pfad_voll.exists() and falsch_name.lower() != bester_zielname_korrekt.lower() else "RENAME"
            print(f"Modus:  {status}")

            antwort = input(f"Zustimmen? (j/n/s): ").lower()

            if antwort == 'j':
                try:
                    # FALL: Zielordner existiert -> MERGEN
                    if ziel_pfad_voll.exists() and falsch_name.lower() != bester_zielname_korrekt.lower():
                        if merge_ordner(quell_pfad_voll, ziel_pfad_voll):
                            print(f"-> Erfolgreich zusammengeführt.")
                            korrektur_zaehler += 1

                    # FALL: Nur Groß-/Kleinschreibung falsch (NTFS-Safe Rename)
                    elif beste_uebereinstimmung == 100:
                        # Path-Objekte erlauben String-Verkettung nicht direkt per +,
                        # daher wandeln wir den Pfad kurz für den Temp-Namen ab
                        temp_pfad = quell_pfad_voll.with_name(falsch_name + "_TEMP")
                        quell_pfad_voll.rename(temp_pfad)
                        temp_pfad.rename(ziel_pfad_voll)
                        print(f"-> Schreibweise korrigiert.")
                        korrektur_zaehler += 1

                    # FALL: Normales Umbenennen
                    else:
                        quell_pfad_voll.rename(ziel_pfad_voll)
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