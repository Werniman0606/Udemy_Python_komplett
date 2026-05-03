import os
import subprocess
from datetime import datetime

# --- KONFIGURATION ---
FFMPEG_EXE = r"C:\Program Files\digiKam\ffmpeg.exe"
DESTINATION_DIR = r"D:\Dashcam\fertigeVideos"
SOURCE_DIR = r"D:\Dashcam"


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
    if not os.path.exists(SOURCE_DIR):
        print("[-] Quellverzeichnis nicht gefunden.")
        return

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
        tours[key].append(os.path.join(SOURCE_DIR, filename))

    # 2. Jede Gruppe einzeln verarbeiten
    for (date, tour_label, cam), files in tours.items():
        files.sort()  # Chronologische Sortierung

        cam_label = "Front" if cam == 'F' else "Rueck"

        # ZIEL: mkv statt ts
        output_filename = f"{date}_{tour_label}_{cam_label}.mkv"
        output_path = os.path.join(DESTINATION_DIR, output_filename)

        print(f"[*] Erstelle {output_filename} ({len(files)} Segmente)...")

        list_file = f"temp_list_{cam}.txt"
        with open(list_file, "w") as f:
            for file in files:
                f.write(f"file '{file.replace('\\', '/')}'\n")

        cmd = [
            FFMPEG_EXE, '-y', '-f', 'concat', '-safe', '0',
            '-i', list_file, '-c', 'copy', output_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"[OK] Gespeichert: {output_path}")
        except subprocess.CalledProcessError:
            print(f"[!] Fehler bei {output_filename}")

        if os.path.exists(list_file):
            os.remove(list_file)


if __name__ == "__main__":
    merge_dual_dashcam()