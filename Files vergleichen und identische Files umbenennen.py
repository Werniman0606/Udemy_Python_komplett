import os
import hashlib

# --- HIER DIE PFADE ANPASSEN ---
QUELLE = "/run/media/marcoj/Laufwerk F/h265"
ZIEL_BACKUP = "/run/media/marcoj/Backup Laufwerk F_2/Laufwerk F/h265"


# -------------------------------

def berechne_hash(dateipfad, blockgroesse=65536):
    """Berechnet den SHA-256 Hash einer Datei in effizienten Blöcken."""
    hasher = hashlib.sha256()
    try:
        with open(dateipfad, 'rb') as f:
            buf = f.read(blockgroesse)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(blockgroesse)
        return hasher.hexdigest()
    except OSError:
        return None


def sync_names_by_hash():
    print("Scanne Quellverzeichnis... Bitte warten...")
    # Struktur: {dateigroesse: {voller_pfad: dateiname}}
    quell_daten = {}
    # Schneller Gegen-Check: {dateigroesse: set(dateiname)}
    quell_namen_nach_groesse = {}

    # 1. Quelle scannen und nach Größe indexieren
    for root, _, files in os.walk(QUELLE):
        for file in files:
            pfad = os.path.join(root, file)
            try:
                groesse = os.path.getsize(pfad)

                if groesse not in quell_daten:
                    quell_daten[groesse] = {}
                    quell_namen_nach_groesse[groesse] = set()

                quell_daten[groesse][pfad] = file
                quell_namen_nach_groesse[groesse].add(file)
            except OSError:
                continue

    print("Scanne Backup-Verzeichnis und gleiche Dateien ab...")
    umbenannte_dateien = 0
    uebersprungene_dateien = 0

    # 2. Backup durchsuchen
    for root, _, files in os.walk(ZIEL_BACKUP):
        for file in files:
            backup_pfad = os.path.join(root, file)
            try:
                backup_groesse = os.path.getsize(backup_pfad)
            except OSError:
                continue

            # Nur prüfen, wenn es in der Quelle überhaupt eine Datei mit dieser Größe gibt
            if backup_groesse in quell_daten:

                # --- DEINE OPTIMIERUNG (SCHNELLSTRASSE) ---
                # Wenn Name UND Größe exakt übereinstimmen, überspringen wir den teuren Hash-Check
                if file in quell_namen_nach_groesse[backup_groesse]:
                    uebersprungene_dateien += 1
                    continue

                # --- HASH-FALLBACK ---
                # Name ist anders, aber Größe passt -> Jetzt prüfen wir den Inhalt via Hash
                backup_hash = berechne_hash(backup_pfad)
                if not backup_hash:
                    continue

                # Wir prüfen nun die Hashes der Quell-Dateien dieser Größe
                for quell_pfad, quell_name in list(quell_daten[backup_groesse].items()):

                    # Hash der Quell-Datei berechnen (falls noch nicht geschehen)
                    if isinstance(quell_name, str):
                        q_hash = berechne_hash(quell_pfad)
                        if q_hash:
                            # Zwischenspeichern für eventuelle weitere Treffer gleicher Größe
                            quell_daten[backup_groesse][quell_pfad] = (quell_name, q_hash)
                        else:
                            continue
                    else:
                        quell_name, q_hash = quell_name

                    # Wenn der Inhalt (Hash) identisch ist...
                    if backup_hash == q_hash:
                        # ...und der Name sich unterscheidet (was er durch die Abkürzung oben eh tut)
                        if file != quell_name:
                            neuer_backup_pfad = os.path.join(root, quell_name)

                            try:
                                print(f"\n[Inhaltlicher Match trotz anderem Namen!]")
                                print(f"Quelle aktuell: {quell_name}")
                                print(f"Backup alt:     {file}")
                                print(f"-> Passe Namen im Backup an zu: {quell_name}")

                                os.rename(backup_pfad, neuer_backup_pfad)
                                umbenannte_dateien += 1
                            except Exception as e:
                                print(f"Fehler beim Umbenennen von {file}: {e}")

                        break

    print(f"\nFertig!")
    print(f"-> {uebersprungene_dateien} bereits identische Dateien (Name & Größe) wurden übersprungen.")
    print(f"-> {umbenannte_dateien} Dateien wurden erfolgreich auf dem Backup-Medium umbenannt.")


if __name__ == "__main__":
    sync_names_by_hash()