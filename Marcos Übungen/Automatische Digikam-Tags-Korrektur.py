# ==============================================================================
# Dateiname: performante_tag_korrektur.py
# Beschreibung: Dieses Skript identifiziert Tippfehler-Varianten von Tags, wählt
#               die häufigste Schreibweise als Master und korrigiert Metadaten
#               und Dateinamen. **Die Korrektur wird nur auf die betroffenen Dateien
#               angewendet**, um die Laufzeit zu optimieren.
# ==============================================================================

import os
import re
import subprocess
import json
from collections import Counter, defaultdict
from fuzzywuzzy import fuzz  # Benötigt: pip install fuzzywuzzy python-Levenshtein

# --- KONFIGURATION ---

# Der Basisordner Ihrer gesamten Bildersammlung
ROOT_FOLDER = r'E:\Bilder\Celebrities'

# PFAD ZU EXIFTOOL.EXE (Muss angepasst werden, falls nicht im PATH!)
EXIFTOOL_PATH = 'exiftool'

# Schwelle (Score von 0 bis 100), ab der Namen als Varianten der gleichen Person gelten.
SIMILARITY_THRESHOLD = 90

# Das Metadatenfeld, das die Personennamen enthält
PERSONEN_TAG_FELD = 'XMP:Subject'


# --- HILFSFUNKTIONEN ---

def extract_persons_from_filename(filename):
    """Extrahiert alle Personennamen aus dem [Name1, Name2]_ Präfix."""
    match = re.match(r'^\[(.+?)\]_', filename)
    if match:
        prefix_content = match.group(1)
        return [name.strip() for name in prefix_content.split(',')]
    return []


def get_xmp_tags(filepath):
    """Ruft ExifTool auf, um die XMP:Subject-Tags zu lesen."""
    tags = []
    cmd = [EXIFTOOL_PATH, f"-{PERSONEN_TAG_FELD}", '-j', filepath]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore')
        if result.stdout.strip():
            output_json = json.loads(result.stdout)
            if output_json and output_json[0] and PERSONEN_TAG_FELD in output_json[0]:
                tag_value = output_json[0][PERSONEN_TAG_FELD]
                if isinstance(tag_value, list):
                    tags = [t.strip() for t in tag_value]
                elif isinstance(tag_value, str):
                    tags = [tag_value.strip()]
    except Exception:
        pass
    return tags


# ----------------------------------------------------------------------
# SCHRITT 1: ANALYSE & ERSTELLUNG DER KORREKTUR-JOBS
# ----------------------------------------------------------------------

def analyze_and_create_jobs(root_dir):
    """
    Analysiert alle Dateien, identifiziert Master/Fehler und erstellt eine
    Liste der spezifischen Korrekturaufträge.
    """
    print("1. Starte Häufigkeitsanalyse und Job-Erstellung...")

    # 1. Sammle alle Namen und ihre Häufigkeit (wie zuvor)
    name_counter = Counter()

    # 2. Sammle Korrekturanweisungen pro Datei
    # jobs = [{'filepath': ..., 'faulty_name': ..., 'master_name': ...}, ...]
    correction_jobs = []

    # Erste Iteration: Nur Dateinamen-Tags analysieren
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            persons = extract_persons_from_filename(filename)
            for person in persons:
                name_counter[person] += 1

    # 3. Master/Fehler-Zuordnung bestimmen (Logik aus dem letzten Skript)
    sorted_names = sorted(name_counter.items(), key=lambda item: item[1], reverse=True)
    master_map = defaultdict(dict)  # {Master: {Faulty: Count, ...}}
    processed_names = set()

    for current_name, count in sorted_names:
        if current_name in processed_names: continue
        master_assigned = False
        for master in list(master_map.keys()):
            score = fuzz.ratio(current_name.lower(), master.lower())
            if score >= SIMILARITY_THRESHOLD:
                master_map[master][current_name] = count
                processed_names.add(current_name)
                master_assigned = True
                break
        if not master_assigned:
            master_map[current_name] = {}
            processed_names.add(current_name)

    # Filtern und Bereinigen der Zuordnung (Master und seine fehlerhaften Varianten)
    name_mapping = {
        master: [faulty for faulty in variants.keys()]
        for master, variants in master_map.items() if variants
    }

    # 4. Zweite Iteration: Nur die wirklich betroffenen Dateien finden (Optimierung!)
    all_faulty_names = set(v for master, fs in name_mapping.items() for v in fs)

    print("-> Erstelle Liste der zu korrigierenden Dateien (Jobs)...")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tif')):
                continue

            filepath = os.path.join(dirpath, filename)

            # Hole die aktuellen XMP-Tags der Datei (WICHTIG: Nicht den Dateinamen-Präfix!)
            current_xmp_tags = get_xmp_tags(filepath)

            for tag in current_xmp_tags:
                if tag in all_faulty_names:
                    # Finde den Master-Namen für diesen fehlerhaften Tag
                    master_name = next((m for m, fs in name_mapping.items() if tag in fs), None)
                    if master_name:
                        correction_jobs.append({
                            'filepath': filepath,
                            'faulty_name': tag,
                            'master_name': master_name
                        })

    # Da eine Datei mehrere fehlerhafte Tags haben kann, Duplikate entfernen (basierend auf Pfad)
    unique_jobs = list({(job['filepath'], job['faulty_name']): job for job in correction_jobs}.values())

    return name_mapping, unique_jobs, name_counter


# ----------------------------------------------------------------------
# SCHRITT 2: KORREKTUR DER XMP-TAGS (PERFORMANT)
# ----------------------------------------------------------------------

def correct_xmp_tags_optimized(correction_jobs):
    """
    Führt die Korrekturen nur für die im Job-Array gelisteten Dateien durch.
    """
    print(f"\n2. Starte Metadaten-Korrektur für {len(correction_jobs)} spezifische Job(s)...")
    corrected_files_count = 0

    for job in correction_jobs:
        filepath = job['filepath']
        old_name = job['faulty_name']
        new_name = job['master_name']

        print(f"-> Verarbeite {os.path.basename(filepath)}: '{old_name}' -> '{new_name}'")

        # Befehl zum Entfernen des falschen Namens und Hinzufügen des Masters
        command = [
            f"-{PERSONEN_TAG_FELD}-={old_name}",
            f"-{PERSONEN_TAG_FELD}+={new_name}",
            f"-MWG-RS:Name-={old_name}",
            f"-MWG-RS:Name+={new_name}",
            '-m'
        ]

        full_command = [EXIFTOOL_PATH] + command + [filepath] + ['-overwrite_original']

        try:
            subprocess.run(full_command, capture_output=True, text=True, check=True)
            corrected_files_count += 1
        except subprocess.CalledProcessError as e:
            print(f"  ❌ FEHLER beim Schreiben der Metadaten: {e.stderr}")
        except FileNotFoundError:
            print(f"  ❌ FEHLER: ExifTool nicht gefunden. Abbruch.")
            return -1

    return corrected_files_count


# ----------------------------------------------------------------------
# SCHRITT 3: KORREKTUR DER DATEINAMEN
# ----------------------------------------------------------------------

def rename_files(correction_mapping):
    """Benennt Dateien mit dem falschen Präfix '[Falscher Name]_...' um."""
    print("\n3. Starte Dateinamen-Korrektur...")
    total_renamed = 0

    # Erstellt ein Mapping nur für Dateinamen-Korrekturen
    for old_name, new_name in [(f, m) for m, fs in correction_mapping.items() for f in fs]:
        pattern = re.compile(re.escape(f"[{old_name}]_"), re.IGNORECASE)

        for root, _, files in os.walk(ROOT_FOLDER):
            for file in files:
                if pattern.match(file):
                    old_path = os.path.join(root, file)
                    new_filename = pattern.sub(f"[{new_name}]_", file, 1)
                    new_path = os.path.join(root, new_filename)

                    try:
                        os.rename(old_path, new_path)
                        print(f"  ✅ UMBENANNT: '{file}' -> **{new_filename}**")
                        total_renamed += 1
                    except FileExistsError:
                        pass  # Ist in diesem Fall ok, da die Datei schon da ist
                    except OSError as e:
                        print(f"  ❌ Fehler beim Umbenennen von {old_path}: {e}")

    return total_renamed


# ----------------------------------------------------------------------
# HAUPTPROGRAMM
# ----------------------------------------------------------------------

if __name__ == "__main__":
    if not os.path.isdir(ROOT_FOLDER):
        print(f"❌ Fehler: Basisordner '{ROOT_FOLDER}' existiert nicht. Bitte Pfad korrigieren.")
        exit()

    # 1. Analyse und Master-Identifizierung (Generiert die Liste der zu korrigierenden Jobs)
    name_mapping, correction_jobs, name_frequencies = analyze_and_create_jobs(ROOT_FOLDER)

    print("\n--- ZUSAMMENFASSUNG DER ANALYSE ---")
    if not name_mapping:
        print("Keine relevanten Tag-Inkonsistenzen über der Schwelle gefunden. Keine Korrektur nötig.")
        exit()

    print(f"Es wurden {len(correction_jobs)} individuelle Metadaten-Korrekturen identifiziert.")

    for master, faulty_names in name_mapping.items():
        print(f"MASTER: **{master}** ({name_frequencies[master]} Vorkommen)")
        for faulty in faulty_names:
            print(f"  ❌ Vorschlag: '{faulty}' ({name_frequencies[faulty]} Vorkommen) wird zu '{master}'")

    print("\n" + "=" * 50)
    input("Bestätigen Sie mit ENTER, um die automatisierte Korrektur (nur betroffene Dateien) zu starten.")
    print("=" * 50)

    # 2. XMP-Metadaten-Korrektur (Performant)
    corrected_xmp_actions = correct_xmp_tags_optimized(correction_jobs)

    # 3. Dateinamen-Korrektur
    renamed_files_count = rename_files(name_mapping)

    print("\n========================================================")
    print("🏁 Prozess abgeschlossen.")
    print(f"Tatsächlich korrigierte Metadaten-Dateien: {corrected_xmp_actions}")
    print(f"Dateien umbenannt: {renamed_files_count}")
    print("========================================================")
    print(
        "NÄCHSTER SCHRITT: Führen Sie in Digikam die **Wartungsfunktion** (Metadaten aller Dateien in Datenbank aktualisieren) aus, um die Datenbank zu bereinigen.")