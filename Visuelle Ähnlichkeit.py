#!/usr/bin/env python3
import os
import sqlite3
from PIL import Image
import imagehash

# ==================== KONFIGURATION ====================
ORDNER_ALT = r"e:\Bilder\Celebrities"  # Dein altes Archiv (z.B. RipMe-Downloads)
ORDNER_NEU = r"d:\Bilder"  # Der neue Ordner (z.B. Gallery-DL)
DB_PFAD = "bild_hashes.db"  # Temporäre SQLite-Datenbank für Stabilität
SCHWELLE = 4  # 0 = bitgenau identisch, bis 4 = visuell gleich
DIREKT_LOESCHEN = False  # Auf True setzen, um neue Duplikate sofort zu löschen!


# =======================================================

def initialisiere_db():
    """Erstellt die temporäre Datenbank-Struktur, falls nicht vorhanden."""
    conn = sqlite3.connect(DB_PFAD)
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS alte_bilder
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       dateiname
                       TEXT,
                       hash_wert
                       TEXT
                   )
                   ''')
    conn.commit()
    return conn


def scanne_altes_archiv(conn):
    """Durchsucht das alte Archiv inklusive aller Unterordner und speichert die Hashes."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM alte_bilder")
    if cursor.fetchone()[0] > 0:
        print("-> Altes Archiv bereits in Datenbank indexiert. Überspringe Scan.")
        return

    print(f"-> Scanne altes Archiv (inkl. Unterordner): {ORDNER_ALT}")

    # os.walk sammelt alle Pfade aus allen Verzweigungen
    alle_pfade = []
    for wurzel, _, dateien in os.walk(ORDNER_ALT):
        for datei in dateien:
            if datei.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                alle_pfade.append(os.path.join(wurzel, datei))

    gesamt = len(alle_pfade)
    if gesamt == 0:
        print("Keine Bilder im alten Archiv gefunden!")
        return

    for index, pfad in enumerate(alle_pfade, 1):
        try:
            with Image.open(pfad) as img:
                # phash erzeugt den resistenten visuellen Fingerabdruck
                v_hash = str(imagehash.phash(img))
                datei_name = os.path.basename(pfad)
                cursor.execute("INSERT INTO alte_bilder (dateiname, hash_wert) VALUES (?, ?)", (datei_name, v_hash))
        except Exception as e:
            print(f"Fehler bei Datei {pfad}: {e}")

        if index % 100 == 0 or index == gesamt:
            print(f"   Fortschritt: {index}/{gesamt} Bilder indexiert...")
            conn.commit()
    conn.commit()


def vergleiche_neue_downloads(conn):
    """Vergleicht die neuen Downloads rekursiv mit dem indexierten alten Archiv."""
    cursor = conn.cursor()
    print(f"\n-> Vergleiche neue Downloads (inkl. Unterordner) aus: {ORDNER_NEU}")

    # Lädt die alten Hashes für maximale Performance beim Abgleich in den Speicher
    cursor.execute("SELECT dateiname, hash_wert FROM alte_bilder")
    alte_daten = [(row[0], imagehash.hex_to_hash(row[1])) for row in cursor.fetchall()]

    if not alte_daten:
        print("Keine alten Vergleichsdaten in der Datenbank vorhanden. Abruch.")
        return

    # Rekursiver Scan des neuen Download-Ordners
    neue_pfade = []
    for wurzel, _, dateien in os.walk(ORDNER_NEU):
        for datei in dateien:
            if datei.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                neue_pfade.append(os.path.join(wurzel, datei))

    gesamt_neu = len(neue_pfade)
    duplikate_zaehler = 0

    for index, pfad in enumerate(neue_pfade, 1):
        try:
            with Image.open(pfad) as img:
                neu_hash = imagehash.phash(img)

            datei_name = os.path.basename(pfad)

            # Abgleich mit der Blacklist aus der Datenbank
            for alt_name, alt_hash in alte_daten:
                # Berechnung der Bit-Differenz (Hamming-Distanz)
                if neu_hash - alt_hash <= SCHWELLE:
                    duplikate_zaehler += 1
                    print(f"[DUPLIKAT] Neu: '{datei_name}' == Alt: '{alt_name}' (Differenz: {neu_hash - alt_hash})")

                    if DIREKT_LOESCHEN:
                        try:
                            os.remove(pfad)  # Löscht das Duplikat im Unterordner
                            print(f"           -> Datei gelöscht.")
                        except Exception as e:
                            print(f"           -> Löschen fehlgeschlagen: {e}")
                    break  # Loop abbrechen, Bild ist als Duplikat identifiziert

        except Exception:
            continue  # Beschädigte Bilddateien einfach überspringen

        if index % 500 == 0 or index == gesamt_neu:
            print(f"   Fortschritt: {index}/{gesamt_neu} neuen Bildern überprüft...")

    print(f"\n==================================================")
    print(f"Fertig! Insgesamt {duplikate_zaehler} visuelle Duplikate gefunden.")
    print(f"==================================================")


if __name__ == "__main__":
    if not os.path.exists(ORDNER_ALT) or not os.path.exists(ORDNER_NEU):
        print("Fehler: Bitte überprüfe die Ordnerpfade in der Konfiguration!")
    else:
        verbindung = initialisiere_db()
        try:
            scanne_altes_archiv(verbindung)
            vergleiche_neue_downloads(verbindung)
        finally:
            verbindung.close()
            # Löscht die temporäre DB-Datei nach Beendigung des Skripts
            if os.path.exists(DB_PFAD):
                try:
                    os.remove(DB_PFAD)
                except:
                    pass