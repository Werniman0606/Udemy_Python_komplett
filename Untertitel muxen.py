import os
import subprocess

# Pfade definieren
# Nutze r"" (Raw-Strings), um Probleme mit Backslashes zu vermeiden
ffmpeg_path = r"C:\Program Files\digiKam\ffmpeg.exe"
source_dir = r"D:\Marco Jahn - Musik"
target_dir = os.path.join(source_dir, "Fertig")

# Zielordner erstellen, falls er nicht existiert
if not os.path.exists(target_dir):
    os.makedirs(target_dir)


def mux_videos():
    if not os.path.exists(ffmpeg_path):
        print(f"Fehler: FFmpeg wurde unter {ffmpeg_path} nicht gefunden!")
        return

    files = os.listdir(source_dir)
    video_extensions = ('.mp4', '.mkv')
    videos = [f for f in files if f.lower().endswith(video_extensions)]

    for video in videos:
        # Basisname ohne Erweiterung
        base_name = os.path.splitext(video)[0]

        # Suche nach einer passenden .srt Datei
        subtitle_file = None
        for f in files:
            # Prüft, ob der Dateiname mit dem Videonamen beginnt und auf .srt endet
            if f.lower().startswith(base_name.lower()) and f.lower().endswith('.srt'):
                subtitle_file = f
                break

        # Nur bearbeiten, wenn ein Untertitel gefunden wurde
        if subtitle_file:
            input_video = os.path.join(source_dir, video)
            input_srt = os.path.join(source_dir, subtitle_file)
            # Zieldatei ist immer .mkv im Unterordner "Fertig"
            output_mkv = os.path.join(target_dir, f"{base_name}.mkv")

            print(f"Muxe: {video} + {subtitle_file} -> Fertig\\{base_name}.mkv")

            # FFmpeg Befehl
            # -i: Inputs
            # -c copy: Video und Audio werden ohne Qualitätsverlust kopiert
            # -c:s srt: Untertitel werden in das mkv-kompatible Format eingebettet
            cmd = [
                ffmpeg_path, '-y',
                '-i', input_video,
                '-i', input_srt,
                '-c', 'copy',
                '-c:s', 'srt',
                output_mkv
            ]

            try:
                # Ausführung (stdout/stderr unterdrückt, außer bei Fehlern)
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    print("Erfolg! Lösche Quelldateien...")
                    os.remove(input_video)
                    os.remove(input_srt)
                else:
                    print(f"FFmpeg Fehler bei {video}: {result.stderr}")
            except Exception as e:
                print(f"Systemfehler bei {video}: {e}")
        else:
            # Optional: Zeigt an, welche Videos übersprungen wurden
            # print(f"Überspringe (kein SRT): {video}")
            pass


if __name__ == "__main__":
    mux_videos()
    print("\nAlle passenden Dateien wurden verarbeitet.")