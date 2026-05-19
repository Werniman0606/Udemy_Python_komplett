import os
import filetype  # Installation: pip install filetype
from pathlib import Path

# =========================== KONFIGURATION ===========================
# Automatische Erkennung des Pfads zum Bilder-Ordner
if os.name == 'nt':  # Windows
    ROOT_FOLDER = Path(r"d:\extracted\rips")
else:  # Linux (CachyOS)
    ROOT_FOLDER = Path("/run/media/marcoj/Laufwerk D/extracted/rips")

# DRY_RUN = True  -> Es wird nur angezeigt, was korrigiert würde.
# DRY_RUN = False -> Die Dateien werden tatsächlich umbenannt.
DRY_RUN = False
# =====================================================================

def get_real_extension(file_path):
    """
    Analysiert den Datei-Header (Magic Bytes) und gibt die
    tatsächliche Endung zurück.
    """
    try:
        kind = filetype.guess(str(file_path))
        if kind:
            return kind.extension
        return None
    except Exception as e:
        print(f"⚠️  Fehler beim Lesen von {file_path.name}: {e}")
        return None


def main():
    # ROOT_FOLDER ist jetzt bereits ein Path-Objekt
    if not ROOT_FOLDER.is_dir():
        print(f"❌ Fehler: Der Ordner '{ROOT_FOLDER}' existiert nicht.")
        return

    mode_label = " [VORSCHAU-MODUS] " if DRY_RUN else " [LIVE-MODUS] "
    print(f"{'=' * 60}\n{mode_label} Starte Analyse in: {ROOT_FOLDER}\n{'=' * 60}")

    checked_count = 0
    renamed_count = 0

    # Durchläuft rekursiv alle Dateien (auch in Unterordnern)
    for file in ROOT_FOLDER.rglob('*'):
        # Nur Dateien bearbeiten, keine Verzeichnisse
        if file.is_file():
            checked_count += 1
            real_ext = get_real_extension(file)

            if real_ext:
                # Aktuelle Endung ohne Punkt (kleingeschrieben)
                current_ext = file.suffix.lstrip('.').lower()

                # Sonderfall-Behandlung: jpg und jpeg als identisch betrachten
                is_same = (current_ext == real_ext) or \
                          (current_ext == 'jpg' and real_ext == 'jpeg') or \
                          (current_ext == 'jpeg' and real_ext == 'jpg')

                if not is_same:
                    new_file = file.with_suffix(f".{real_ext}")

                    # Falls die Zieldatei schon existiert, Umbenennung verhindern
                    if new_file.exists():
                        print(f"Skipped: {file.name} -> {real_ext} (Ziel existiert bereits)")
                        continue

                    print(f"✅ Gefunden: '{file.name}' ist eigentlich eine .{real_ext} Datei")

                    if not DRY_RUN:
                        try:
                            file.rename(new_file)
                            renamed_count += 1
                        except Exception as e:
                            print(f"   ❌ Fehler beim Umbenennen: {e}")
                    else:
                        # Im Dry Run zählen wir die Vorschläge mit
                        renamed_count += 1

    print("-" * 60)
    print(f"Analyse beendet.")
    print(f"Geprüfte Dateien: {checked_count}")

    if DRY_RUN:
        print(f"Mögliche Korrekturen (nicht ausgeführt): {renamed_count}")
        print("\n--> Setze 'DRY_RUN = False' im Skript, um die Änderungen anzuwenden.")
    else:
        print(f"Tatsächlich umbenannt: {renamed_count}")
    print("-" * 60)


if __name__ == "__main__":
    main()
