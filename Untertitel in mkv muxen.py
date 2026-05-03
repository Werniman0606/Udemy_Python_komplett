import os
import subprocess
from pathlib import Path

def mux_with_ffmpeg(root_dir):
    # Falls ffmpeg nicht in den Umgebungsvariablen ist, hier den Pfad eintragen
    # z.B. r"C:\ffmpeg\bin\ffmpeg.exe"
    ffmpeg_exe = "ffmpeg"

    base_path = Path(root_dir)

    for mkv_file in base_path.rglob("*.mkv"):
        if mkv_file.name.startswith("fixed_"): continue
        srt_file = mkv_file.with_suffix(".srt")

        if srt_file.exists():
            output_file = mkv_file.parent / f"fixed_{mkv_file.name}"
            print(f"FFmpeg Muxing: {mkv_file.name}")

            # FFmpeg Befehl:
            # -i (input)
            # -c copy (Video/Audio nicht neu kodieren, nur kopieren)
            # -c:s srt (Untertitel als srt einbinden)
            command = [
                ffmpeg_exe,
                "-i", str(mkv_file),
                "-i", str(srt_file),
                "-c", "copy",
                "-c:s", "srt",
                "-disposition:s:0", "default", # Untertitel als Standard setzen
                str(output_file),
                "-y" # Bestehende Ausgabedatei überschreiben
            ]

            try:
                # Wir unterdrücken die riesige FFmpeg-Log-Ausgabe (loglevel error)
                result = subprocess.run(command, capture_output=True, text=True)

                if result.returncode == 0:
                    print("   -> ERFOLG!")
                    # mkv_file.unlink() # Erst aktivieren, wenn alles läuft!
                    # srt_file.unlink()
                else:
                    print(f"   -> FFmpeg Fehler: {result.stderr}")
            except Exception as e:
                print(f"   -> Systemfehler: {e}")

if __name__ == "__main__":
    mux_with_ffmpeg(r"d:\extracted")