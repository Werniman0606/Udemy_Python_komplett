import os
import re
import platform
from pathlib import Path


def get_base_path():
    """Erkennt das Betriebssystem und gibt den passenden Basispfad zurück."""
    current_os = platform.system()
    if current_os == "Linux":
        return Path("/run/media/marcoj/Laufwerk E/Bilder/Celebrities")
    elif current_os == "Windows":
        return Path(r"E:\Bilder\Celebrities")
    else:
        raise OSError(f"Nicht unterstütztes Betriebssystem: {current_os}")


def clean_filename(filename):
    """
    Erkennt beide Muster extrem präzise (nur IDs, die mit '1' beginnen).
    Gibt den bereinigten Namen ohne Endung zurück oder None, wenn kein Muster passt.
    """
    # -------------------------------------------------------------------------
    # MUSTER B: Bereits sortiert mit eckigen Klammern (ID MUSS mit 1 beginnen und 7 Zeichen haben)
    # Beispiel: "[Linda Schmitz]_1mgh8h2-Linda Schmitz 1970s-94qxojjelsgf"
    # Ziel:     "[Linda Schmitz]_Linda Schmitz 1970s"
    # -------------------------------------------------------------------------
    if filename.startswith("["):
        # ^(\[.*?\])_        -> Gruppe 1: Der Teil in eckigen Klammern
        # 1[a-z0-9]{6}       -> Die Reddit-ID (beginnt zwingend mit 1, gefolgt von 6 Zeichen)
        # \-                 -> Der Bindestrich nach der ID
        # (.*?)              -> Gruppe 2: Der eigentliche Name
        # (?:\-[a-z0-9]+)?$  -> Optional: Der ID-Anhang am Ende (z.B. -94qxojjelsgf)
        pattern_brackets = r"^(\[.*?\])_1[a-z0-9]{6}\-(.*?)(?:\-[a-z0-9]+)?$"
        match = re.match(pattern_brackets, filename, re.IGNORECASE)

        if match:
            brackets = match.group(1)
            clean_text = match.group(2).strip()
            if clean_text:
                return f"{brackets}_{clean_text}"

    # -------------------------------------------------------------------------
    # MUSTER A: Neue Downloads (ID MUSS mit 1 beginnen und 7 Zeichen haben)
    # Beispiel: "1q3ved6 Leanna Decker" oder "1tejko1 02 Fernanda brandao"
    # Ziel:     "Leanna Decker" bzw. "Fernanda brandao"
    # -------------------------------------------------------------------------
    # ^1[a-z0-9]{6}      -> Findet NUR IDs, die mit 1 starten und 7 Zeichen lang sind
    # \s+                -> Mindestens ein Leerzeichen danach
    # (?:(?:\d{2})\s+)?  -> Optional: Zweistellige Zahl (z.B. "02 ")
    # (.*)$              -> Gruppe 1: Der restliche Name
    pattern_new = r"^1[a-z0-9]{6}\s+(?:(?:\d{2})\s+)?(.*)$"
    match = re.match(pattern_new, filename, re.IGNORECASE)

    if match:
        clean_text = match.group(1).strip()
        if clean_text:
            return clean_text

    return None


def rename_files():
    try:
        base_path = get_base_path()
    except OSError as e:
        print(f"Fehler bei der Pfadermittlung: {e}")
        return

    if not base_path.exists():
        print(f"Fehler: Der Pfad '{base_path}' existiert nicht.")
        return

    print(f"Starte SICHERE Bereinigung in: {base_path}\n" + "-" * 50)

    renamed_count = 0
    skipped_count = 0

    for file_path in base_path.rglob("*"):
        if not file_path.is_file():
            continue

        old_name = file_path.stem
        extension = file_path.suffix

        cleaned_name = clean_filename(old_name)

        # Wenn kein Muster matcht oder Name gleich bleibt -> Überspringen
        if not cleaned_name or cleaned_name == old_name:
            skipped_count += 1
            continue

        parent_dir = file_path.parent
        new_file_path = parent_dir / f"{cleaned_name}{extension}"

        # Kollisionsschutz vor der Endung
        counter = 1
        while new_file_path.exists():
            new_file_path = parent_dir / f"{cleaned_name}_{counter}{extension}"
            counter += 1

        try:
            file_path.rename(new_file_path)
            print(f"Bereinigt: '{file_path.name}' -> '{new_file_path.name}'")
            renamed_count += 1
        except Exception as e:
            print(f"Fehler bei '{file_path.name}': {e}")

    print("-" * 50)
    print(f"Fertig! {renamed_count} Dateien umbenannt. {skipped_count} Dateien übersprungen/unverändert.")


if __name__ == "__main__":
    rename_files()