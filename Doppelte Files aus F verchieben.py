import os
import shutil

# --- HIER DIE PFADE ANPASSEN ---
QUELLE = "/run/media/marcoj/Laufwerk F"
ZIEL_BACKUP = "/run/media/marcoj/Backup Laufwerk F_2/Laufwerk F"
VERSCHOBEN = ("/run/media/marcoj/Laufwerk F/verschoben")


# -------------------------------

def check_and_move():
    # 1. Alle Dateinamen auf der Backupplatte einsammeln
    print("Scanne Backup-Medium... Bitte warten...")
    backup_files = set()
    for root, _, files in os.walk(ZIEL_BACKUP):
        for file in files:
            backup_files.add(file)

    print(f"-> {len(backup_files)} Dateien auf dem Backup gefunden.")
    print("Gleiche Quelle ab und verschiebe Duplikate...")

    verarbeitete_dateien = 0

    # 2. Quelle durchsuchen und bei Namensgleichheit verschieben
    for root, _, files in os.walk(QUELLE):
        # Bloß nicht den eigenen "verschoben"-Ordner mitscannen
        if VERSCHOBEN in root:
            continue

        for file in files:
            if file in backup_files:
                # Pfad auf der Quelle ermitteln
                quell_datei = os.path.join(root, file)

                # Relativen Pfad berechnen, um die Struktur zu erhalten
                relativer_pfad = os.path.relpath(root, QUELLE)
                ziel_ordner = os.path.join(VERSCHOBEN, relativer_pfad)

                # Ziel-Ordnerstruktur erstellen, falls sie noch nicht existiert
                os.makedirs(ziel_ordner, exist_ok=True)

                # Datei physisch verschieben
                shutil.move(quell_datei, os.path.join(ziel_ordner, file))
                verarbeitete_dateien += 1

    print(f"\nFertig! {verarbeitete_dateien} Dateien wurden erfolgreich nach '{VERSCHOBEN}' verschoben.")


if __name__ == "__main__":
    check_and_move()