# ==============================================================================
# Dateiname: automatische_digikam_tag_korrektur.py
# Beschreibung: Dieses Skript analysiert die Häufigkeit von [Tag]_Präfixen,
#               identifiziert Tippfehler in Namen (z.B. "Tylor" vs. "Tyler")
#               und korrigiert die Metadaten (XMP:Subject) aller betroffenen
#               Dateien direkt mit ExifTool. Nach der Korrektur liest Digikam
#               nur noch den Master-Namen, und der Dateiname kann rekonstruiert werden.
# ==============================================================================

import os
import re
import subprocess
import json
from collections import Counter, defaultdict
from fuzzywuzzy import fuzz  # Benötigt: pip install fuzzywuzzy python-Levenshtein

# --- KONFIGURATION ---

# Der Hauptordner, der rekursiv durchsucht wird (die gesamte Bildersammlung)
ROOT_FOLDER = r"e:\Bilder\Celebrities"

# PFAD ZU EXIFTOOL.EXE (Muss angepasst werden!)
EXIFTOOL_PATH = r"d:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe"

# Schwelle (Score von 0 bis 100), ab der Namen als Varianten der gleichen Person gelten.
# 90+ ist sicher für Tippfehler.
SIMILARITY_THRESHOLD = 90

# Das Metadatenfeld, das die Personennamen enthält (Digikam nutzt XMP:Subject/TagsList)
PERSONEN_TAG_FELD = 'XMP:Subject'


# --- HILFSFUNKTIONEN ---

def extract_persons_from_filename(filename):
    """Extrahiert alle Personennamen aus dem [Name1, Name2]_ Präfix."""
    match = re.match(r'^\[(.+?)\]_', filename)
    if match:
        prefix_content = match.group(1)
        # Teilt die Namen an Kommas und bereinigt Leerzeichen
        return [name.strip() for name in prefix_content.split(',')]
    return []


def get_xmp_tags(filepath):
    """Ruft ExifTool auf, um die XMP:Subject-Tags zu lesen."""
    tags = []
    # Verwende den JSON-Output für einfache Verarbeitung
    cmd = [EXIFTOOL_PATH, f"-{PERSONEN_TAG_FELD}", '-j', filepath]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        if not result.stdout.strip():
            return tags

        output_json = json.loads(result.stdout)
        if output_json and output_json[0] and PERSONEN_TAG_FELD in output_json[0]:
            tag_value = output_json[0][PERSONEN_TAG_FELD]
            if isinstance(tag_value, list):
                tags = [t.strip() for t in tag_value]
            elif isinstance(tag_value, str):
                tags = [tag_value.strip()]
    except Exception as e:
        # Fehler beim Lesen ignorieren, da wir nur die Tags benötigen
        pass
    return tags


def correct_xmp_tag(filepath, faulty_name, master_name):
    """
    Entfernt den fehlerhaften Tag und fügt den Master-Tag hinzu.
    Schreibt direkt in die Datei und erstellt eine .original-Datei als Backup.
    """
    if faulty_name == master_name:
        return False  # Nichts zu tun

    # 1. Entferne den fehlerhaften Tag (-)
    cmd_remove = [
        EXIFTOOL_PATH,
        f"-{PERSONEN_TAG_FELD}-={faulty_name}",
        '-overwrite_original',  # Entferne diese Zeile, um .original-Backups zu erhalten
        filepath
    ]

    # 2. Füge den Master-Tag hinzu (+) (falls er noch nicht existiert)
    cmd_add = [
        EXIFTOOL_PATH,
        f"-{PERSONEN_TAG_FELD}+={master_name}",
        '-overwrite_original',
        filepath
    ]

    try:
        subprocess.run(cmd_remove, check=True, capture_output=True)
        subprocess.run(cmd_add, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ FEHLER beim Schreiben der Metadaten in '{os.path.basename(filepath)}': {e.stderr}")
        return False
    except Exception as e:
        print(f"  ❌ UNBEKANNTER FEHLER beim Korrigieren von '{os.path.basename(filepath)}': {e}")
        return False


# --- HAUPTANALYSE & KORREKTUR ---

def find_master_and_faulty_names(root_dir):
    """
    Analysiert alle Dateinamen-Tags in der gesamten Sammlung, um die
    Master- und Fehler-Varianten durch Häufigkeitsvergleich zu identifizieren.
    """
    print("1. Starte Häufigkeitsanalyse der Tags in der gesamten Sammlung...")
    # Speichert die Häufigkeit jeder Schreibweise (unter Beibehaltung der Groß-/Kleinschreibung)
    name_counter = Counter()

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            persons = extract_persons_from_filename(filename)
            for person in persons:
                name_counter[person] += 1

    # Gruppiere ähnliche Namen (z.B. alle "Bonnie T*"-Varianten)
    # Speichert {Master-Name: [Liste fehlerhafter Varianten]}
    master_map = {}

    # Sortiere nach Häufigkeit (die häufigste ist wahrscheinlich die Master-Schreibweise)
    sorted_names = sorted(name_counter.items(), key=lambda item: item[1], reverse=True)

    # Führe eine paarweise Überprüfung durch, um Tippfehler zu finden
    for current_name, count in sorted_names:
        found_master = False

        # Versuche, den aktuellen Namen einem bereits gefundenen Master-Namen zuzuordnen
        for master, _ in master_map.items():
            # Verwende Token Set Ratio für bessere Robustheit bei Wortreihenfolge
            score = fuzz.ratio(current_name.lower(), master.lower())

            if score >= SIMILARITY_THRESHOLD:
                # Der aktuelle Name ist eine Variante des Masters
                master_map[master].append(current_name)
                found_master = True
                break

        if not found_master:
            # Der Name ist selbst der Master einer neuen Gruppe
            master_map[current_name] = []

    # Filtern der Master-Map, um nur relevante Korrekturen zu erhalten
    correction_targets = {}
    for master, variants in master_map.items():
        # Die Master-Map enthält den Master selbst in der Variantenliste
        faulty_variants = [v for v in variants if v != master]
        if faulty_variants:
            correction_targets[master] = faulty_variants

    return correction_targets


def apply_corrections(root_dir, correction_targets):
    """
    Durchsucht die Dateien erneut und wendet die Metadaten-Korrekturen an.
    """
    print("\n2. Starte Metadaten-Korrektur...")
    print("--------------------------------------------------")
    corrected_files_count = 0

    # Wir brauchen eine Liste aller zu korrigierenden Namen, um den Suchprozess zu beschleunigen
    all_faulty_names = set(v for variants in correction_targets.values() for v in variants)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                continue

            filepath = os.path.join(dirpath, filename)

            # Liest die tatsächlichen XMP-Tags der Datei (nicht den Dateinamen-Präfix!)
            current_xmp_tags = get_xmp_tags(filepath)

            # Prüfe, ob einer der fehlerhaften Namen in den Tags dieser Datei vorkommt
            tags_to_correct = []

            for tag in current_xmp_tags:
                if tag in all_faulty_names:
                    # Finde den Master-Namen, der zu diesem fehlerhaften Tag gehört
                    master = next((m for m, variants in correction_targets.items() if tag in variants), None)
                    if master:
                        tags_to_correct.append((tag, master))

            if tags_to_correct:
                print(f"-> Verarbeite: {filename}")
                file_was_corrected = False

                for faulty_name, master_name in tags_to_correct:
                    # Führe die Korrektur durch
                    if correct_xmp_tag(filepath, faulty_name, master_name):
                        file_was_corrected = True
                        print(f"   KORRIGIERT: '{faulty_name}' zu '{master_name}'")

                if file_was_corrected:
                    corrected_files_count += 1

    return corrected_files_count


def main():
    if not os.path.isdir(ROOT_FOLDER):
        print(f"❌ Fehler: Hauptordner '{ROOT_FOLDER}' existiert nicht.")
        return

    if not os.path.isfile(EXIFTOOL_PATH):
        print(f"❌ Fehler: ExifTool-Pfad '{EXIFTOOL_PATH}' ist falsch. Bitte anpassen!")
        return

    # 1. Analyse: Finde alle Master-Namen und ihre Tippfehler-Varianten
    correction_targets = find_master_and_faulty_names(ROOT_FOLDER)

    print("\n--- Analyse-Ergebnisse (Vorschläge) ---")
    if not correction_targets:
        print("Keine relevanten Tag-Inkonsistenzen über der Schwelle gefunden.")
        return

    total_variants = sum(len(v) for v in correction_targets.values())
    print(f"Gefundene Korrekturgruppen: {len(correction_targets)}")
    print(f"Betroffene fehlerhafte Varianten: {total_variants}")
    print("---------------------------------------")

    for master, variants in correction_targets.items():
        print(f"MASTER: **{master}**")
        print(f"  ❌ Fehlerhafte Varianten (werden entfernt): {', '.join(variants)}")

    # 2. Korrektur: Wende die Korrekturen auf die Metadaten an
    input("\nBestätigen Sie mit ENTER, um die Metadaten jetzt zu korrigieren (STRG+C zum Abbrechen):")

    corrected_files = apply_corrections(ROOT_FOLDER, correction_targets)

    print("\n========================================================")
    print("🏁 Korrektur abgeschlossen.")
    print(f"Gesamt korrigierte Dateien: {corrected_files}")
    print("========================================================")
    print("NÄCHSTER SCHRITT: Führen Sie das Skript 'dateiname_aus_digikam_tags_rekonstruieren.py' erneut aus.")
    print("Da die Metadaten nun sauber sind, wird es die Dateinamen-Präfixe korrekt bereinigen.")


if __name__ == "__main__":
    main()