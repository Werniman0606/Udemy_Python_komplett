#!/usr/bin/env python3
import subprocess
import os

# ================= CACHYOS KONFIGURATION =================
# Pfade direkt auf deinen Desktop gemappt
INPUT_FILE = "/home/marcoj/Desktop/youtube_tabs.txt"
CLEAN_FILE = "/home/marcoj/Desktop/youtube_tabs_working.txt"
DEAD_FILE = "/home/marcoj/Desktop/youtube_tabs_dead.txt"
# =========================================================

# Sicherheitscheck: Existiert die Ausgangsdatei?
if not os.path.exists(INPUT_FILE):
    print(f"Fehler: Die Datei '{INPUT_FILE}' wurde nicht auf deinem Desktop gefunden!")
    print("Bitte stelle sicher, dass die exportierte Link-Liste dort liegt.")
    exit(1)

# Sicherheitscheck: Ist yt-dlp installiert?
try:
    subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, check=True)
except (subprocess.CalledProcessError, FileNotFoundError):
    print("Fehler: 'yt-dlp' ist nicht installiert oder im PATH unauffindbar.")
    print("Du kannst es im CachyOS-Terminal schnell nachinstallieren mit:")
    print("sudo pacman -S yt-dlp")
    exit(1)

print(f"Lese URLs aus: {INPUT_FILE}")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    urls = f.read().splitlines()

print(f"{len(urls)} Zeilen geladen. Starte Überprüfung via yt-dlp...\n")

# Falls alte Ergebnisdateien existieren, löschen wir sie vor dem Durchlauf,
# damit die Ergebnisse nicht an alte Listen angehängt werden.
for f_path in [CLEAN_FILE, DEAD_FILE]:
    if os.path.exists(f_path):
        os.remove(f_path)

for url in urls:
    url = url.strip()
    if not url:
        continue  # Leere Zeilen überspringen

    # Filtern, ob es sich überhaupt um einen Video-Link handelt
    if "youtube.com/watch" in url or "youtu.be/" in url:
        # yt-dlp prüft nur die Metadaten (-g wirft die Video-URL aus, falls erreichbar)
        result = subprocess.run(["yt-dlp", "-g", url], capture_output=True, text=True)

        if result.returncode == 0:
            # Video ist online und erreichbar
            print(f"  [ONLINE]      {url}")
            with open(CLEAN_FILE, "a", encoding="utf-8") as f_ok:
                f_ok.write(url + "\n")
        else:
            # Video ist privat, gelöscht, Region-locked oder Kanal existiert nicht mehr
            print(f"❌ [TOT/PRIVAT]  {url}")
            with open(DEAD_FILE, "a", encoding="utf-8") as f_dead:
                f_dead.write(url + "\n")

print("\n" + "=" * 50)
print("Überprüfung abgeschlossen!")
print(f"-> Erreichbare Videos: {CLEAN_FILE}")
print(f"-> Tote/Private Videos: {DEAD_FILE}")
print("=" * 50)