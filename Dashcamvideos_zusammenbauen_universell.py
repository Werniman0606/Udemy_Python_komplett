import os
import subprocess
from pathlib import Path

# --- KONFIGURATION & BETRIEBSSYSTEM-ERKENNUNG ---
if os.name == 'nt':  # Windows
    FFMPEG_EXE = Path(r"C:\Program Files\digiKam\ffmpeg.exe")
    SOURCE_DIR = Path(r"D:\Dashcam")
    DESTINATION_DIR = Path(r"D:\Dashcam\fertigeVideos")
else:  # Linux (CachyOS)
    # Unter Linux nutzen wir das globale ffmpeg aus dem System
    FFMPEG_EXE = Path("/usr/bin/ffmpeg")
    # Falls es dort nicht liegt, sucht 'which' danach – sonst Standardfall:
    if not FFMPEG_EXE.exists():
        FFMPEG_EXE = Path("ffmpeg")

    SOURCE_DIR = Path("/run/media/marcoj/Laufwerk D/Dashcam")
    DESTINATION_DIR = Path("/run/media/marcoj/Laufwerk D/Dashcam/fertigeVideos")


def get_tour_label(filename):
    """
    Extrahiert die Uhrzeit aus dem Dateinamen (z.B. 20260317_123000F.ts)
    und ordnet sie einem Namen zu.
    """
    try:
        # Extrahiert den Teil nach dem Unterstrich (z.B. 123000)
        time_part = filename.split('_')[1][:6]
        hour = int(time_part[:2])

        # HIER DEINE ZEITEN FESTLEGEN:
        if hour < 10:
            return "Morgentour"
        elif 11 <= hour < 18:
            return "Mittagstour"
        else:
            return "Nachmittagstour"
    except (IndexError, ValueError):
        return "UnbekannteTour"


def merge_dual_dashcam():
    # .exists() funktioniert perfekt mit Path-Objekten
    if not SOURCE_DIR.exists():
        print(f"[-] Quellverzeichnis nicht gefunden: {SOURCE_DIR}")
        return

    # Zielordner erstellen, falls er noch nicht existiert
    DESTINATION_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Alle .ts Dateien einlesen
    all_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.ts')]

    # Struktur: {(Datum, Tour_Label, Kamera_Kürzel): [Dateiliste]}
    tours = {}

    for filename in all_files:
        date_part = filename.split('_')[0]
        tour_label = get_tour_label(filename)
        # Das letzte Zeichen vor der Endung ist die Kamera (F oder R)
        camera_code = filename.replace('.ts', '')[-1]

        key = (date_part, tour_label, camera_code)
        if key not in tours:
            tours[key] = []

        # Pfad plattformunabhängig zusammenbauen
        tours[key].append(SOURCE_DIR / filename)

    # 2. Jede Gruppe einzeln verarbeiten
    for (date, tour_label, cam), files in tours.items():
        files.sort()  # Chronologische Sortierung

        cam_label = "Front" if cam == 'F' else "Rueck"

        # ZIEL: mkv statt ts
        output_filename = f"{date}_{tour_label}_{cam_label}.mkv"
        output_path = DESTINATION_DIR / output_filename

        print(f"[*] Erstelle {output_filename} ({len(files)} Segmente)...")

        list_file = f"temp_list_{cam}.txt"
        with open(list_file, "w", encoding="utf-8") as f:
            for file in files:
                # ffmpeg verlangt im concat-File zwingend Vorwärts-Schrägstriche (/),
                # .as_posix() erzwingt diese Schreibweise automatisch, egal welches OS!
                f.write(f"file '{file.as_posix()}'\n")

        # cmd-Liste akzeptiert Path-Objekte, wir wandeln sie für subprocess in Strings um
        cmd = [
            str(FFMPEG_EXE), '-y', '-f', 'concat', '-safe', '0',
            '-i', list_file, '-c', 'copy', str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[OK] Gespeichert: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"[!] Fehler bei {output_filename}")
            # Zeigt den echten ffmpeg-Fehler im Terminal, falls mal was schiefgeht
            if e.stderr:
                print(e.stderr.decode(errors='ignore'))

        if os.path.exists(list_file):
            os.remove(list_file)


if __name__ == "__main__":
    merge_dual_dashcam()

⁰