import os
import subprocess
import glob

# --- KONFIGURATION ---
ROOT_DIR = r'f:\IT-Videos'
MKVMERGE_PATH = r'C:\Program Files\MKVToolNix\mkvmerge.exe'


# ---------------------

def process_mkv_files(root_path):
    for subdir, dirs, files in os.walk(root_path):
        for file in files:
            # Wir suchen nach MKV-Dateien
            if file.lower().endswith('.mkv'):
                video_path = os.path.join(subdir, file)
                # Den reinen Dateinamen ohne .mkv holen
                base_name = os.path.splitext(file)[0]

                # Wir suchen nach SRT-Dateien, die exakt so heißen wie das Video...
                # ODER die mit dem Videonamen plus einem Punkt beginnen (z.B. .Englisch.srt)
                # Das verhindert, dass "Video 1.mkv" die Untertitel von "Video 10.srt" greift.
                srt_pattern = os.path.join(subdir, f"{base_name}*.srt")
                potential_srts = glob.glob(srt_pattern)

                # Wir filtern die Liste manuell, um sicherzugehen, dass es
                # entweder "Name.srt" oder "Name.Irgendetwas.srt" ist.
                matching_srts = [
                    s for s in potential_srts
                    if os.path.basename(s) == f"{base_name}.srt"
                       or os.path.basename(s).startswith(f"{base_name}.")
                ]

                if matching_srts:
                    # Nimm die erste gefundene passende Untertiteldatei
                    srt_path = matching_srts[0]
                    srt_filename = os.path.basename(srt_path)

                    output_file = os.path.join(subdir, f"{base_name}_temp.mkv")

                    print(f"Gefunden: {file}")
                    print(f"Muxe mit: {srt_filename}")

                    cmd = [
                        MKVMERGE_PATH,
                        '-o', output_file,
                        video_path,
                        srt_path
                    ]

                    try:
                        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

                        if result.returncode == 0:
                            # Sicherheitshalber prüfen, ob die Temp-Datei erstellt wurde
                            if os.path.exists(output_file):
                                os.remove(video_path)
                                os.remove(srt_path)
                                os.rename(output_file, video_path)
                                print(f"Erfolg: Untertitel integriert.\n")

                    except subprocess.CalledProcessError as e:
                        print(f"FEHLER bei {file}: {e.stderr}")
                        if os.path.exists(output_file):
                            os.remove(output_file)
                else:
                    # Hier passiert nichts, wenn kein passender Untertitel da ist
                    pass


if __name__ == "__main__":
    if os.path.exists(ROOT_DIR):
        print("--- Suche startet ---\n")
        process_mkv_files(ROOT_DIR)
        print("--- Fertig! ---")
    else:
        print(f"Pfad nicht gefunden: {ROOT_DIR}")