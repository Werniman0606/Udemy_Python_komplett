import os
import subprocess
from pathlib import Path
import re


def radical_srt_fix(srt_path):
    """Baut die SRT komplett neu und löscht ALLES, was mkvmerge stören könnte."""
    try:
        with open(srt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 1. Alle exotischen Leerzeichen (wie \xa0) durch normale Leerzeichen ersetzen
        content = content.replace('\xa0', ' ')
        lines = content.splitlines()

        new_content = []
        for line in lines:
            line = line.strip()
            # Zeitstempel-Zeile finden und radikal säubern
            if "-->" in line:
                # Suche alle Zeit-Muster (00:00:00,000)
                times = re.findall(r'\d{1,2}:\d{2}:\d{2}[.,]\d{3}', line)
                if len(times) == 2:
                    line = f"{times[0].replace('.', ',')} --> {times[1].replace('.', ',')}"
                elif len(times) == 1:
                    # Falls Endzeit fehlt, Startzeit + 3 Sekunden
                    start = times[0].replace('.', ',')
                    line = f"{start} --> {start[:-3]}999"
                else:
                    continue  # Kaputte Zeitzeile überspringen

            if line:
                new_content.append(line)

        with open(srt_path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write("\n\n".join(new_content))  # Doppelte Zeilenumbrüche für SRT-Standard
        return True
    except:
        return False


def mux_subtitles(root_dir):
    # Pfad anpassen, falls nötig
    mkvmerge_exe = r"C:\Program Files\MKVToolNix\mkvmerge.exe"
    base_path = Path(root_dir)

    for mkv_file in base_path.rglob("*.mkv"):
        if mkv_file.name.startswith("fixed_"): continue
        srt_file = mkv_file.with_suffix(".srt")

        if srt_file.exists():
            print(f"Versuche Hard-Fix: {mkv_file.name}")
            radical_srt_fix(srt_file)

            output_file = mkv_file.parent / f"fixed_{mkv_file.name}"

            # Die "Erzwingen"-Syntax für mkvmerge
            command = [
                mkvmerge_exe,
                "-o", str(output_file),
                str(mkv_file),
                "--language", "0:ger",  # Wir setzen die Sprache fest auf Deutsch
                "--track-name", "0:Untertitel",
                str(srt_file)
            ]

            result = subprocess.run(command, capture_output=True, text=True, errors='ignore')

            if result.returncode == 0:
                print("   -> ERFOLG!")
                try:
                    # Optional: Originale erst löschen, wenn du sicher bist!
                    # os.remove(mkv_file)
                    # os.remove(srt_file)
                    pass
                except:
                    pass
            else:
                # Jetzt loggen wir den FEHLER-CODE von mkvmerge im Detail
                print(f"   -> mkvmerge Error-Log: {result.stderr.strip()}")


if __name__ == "__main__":
    mux_subtitles(r"d:\extracted")