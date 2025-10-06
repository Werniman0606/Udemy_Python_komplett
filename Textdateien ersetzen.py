import os
import shutil

# --- Konfiguration ---
# Der Hauptordner mit der Ziel-Struktur und den .txt-Dateien
SOURCE_BASE_DIR = r"d:\extracted\Inzest\SeVac 2000-2025"
# Der Ordner, in dem alle .pdf-Dateien (ohne Unterordner) liegen
PDF_POOL_DIR = r"d:\extracted\Inzest2"


# ---------------------

def migrate_and_replace_files(source_dir, pdf_pool_dir):
    """
    Durchsucht den Quellordner nach .txt-Dateien, sucht nach passenden
    .pdf-Dateien im PDF-Pool-Ordner, verschiebt die PDF und löscht die TXT.
    """
    print(f"Starte Suche in: {source_dir}")
    print(f"PDF-Quellordner: {pdf_pool_dir}\n")

    # Durchlaufe den SOURCE_BASE_DIR rekursiv
    for root, _, files in os.walk(source_dir):
        for filename in files:
            # Nur .txt-Dateien verarbeiten
            if filename.lower().endswith('.txt'):
                # 1. Dateinamen und Pfade ermitteln
                txt_full_path = os.path.join(root, filename)

                # Der Dateiname ohne Endung (.txt)
                # 'Beispiel.txt' -> 'Beispiel'
                base_name = os.path.splitext(filename)[0]

                # Der gesuchte PDF-Dateiname ('Beispiel.pdf')
                pdf_filename = base_name + '.pdf'

                # Der vollständige Pfad zur PDF im Pool-Ordner
                pdf_pool_path = os.path.join(pdf_pool_dir, pdf_filename)

                # Der Zielpfad für die PDF (gleicher Ordner wie die TXT)
                pdf_target_path = os.path.join(root, pdf_filename)

                # 2. Prüfen, ob die passende PDF-Datei existiert
                if os.path.exists(pdf_pool_path):
                    print(f"*** Treffer gefunden: {base_name} ***")
                    print(f"  TXT-Pfad: {txt_full_path}")
                    print(f"  PDF-Pool: {pdf_pool_path}")

                    try:
                        # 3. PDF verschieben (Ausschneiden und Einfügen)
                        # shutil.move ist atomarer als copy + delete
                        shutil.move(pdf_pool_path, pdf_target_path)

                        # 4. Ursprüngliche TXT-Datei löschen
                        os.remove(txt_full_path)

                        print(f"  ERFOLG: {pdf_filename} verschoben nach {root}.")
                        print(f"          {filename} gelöscht.\n")

                    except Exception as e:
                        print(f"  FEHLER beim Verarbeiten von {base_name}: {e}\n")
                else:
                    # Optional: Zeigt an, wenn keine passende PDF gefunden wurde
                    # print(f"Keine passende PDF für {filename} im Pool gefunden.")
                    pass


# Skript ausführen
migrate_and_replace_files(SOURCE_BASE_DIR, PDF_POOL_DIR)
print("--- Vorgang abgeschlossen ---")