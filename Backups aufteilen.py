import os


def get_dir_size(path):
    """Berechnet die Gesamtgröße eines Ordners in Bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Überspringe symbolische Links
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def plan_backup_chunks(source_dir, max_disk_size_gb):
    # Umrechnung von GB in Bytes
    MAX_DISK_SIZE = max_disk_size_gb * 1024 * 1024 * 1024

    # Schritt 1: Größe aller Top-Level-Ordner ermitteln
    print("Scanne Quellverzeichnis und berechne Ordnergrößen...")
    items = []
    for item in os.listdir(source_dir):
        full_path = os.path.join(source_dir, item)
        if os.path.isdir(full_path):
            size = get_dir_size(full_path)
            items.append({'name': item, 'size': size})
        elif os.path.isfile(full_path):
            # Einzelne Dateien direkt auf der obersten Ebene
            size = os.path.getsize(full_path)
            items.append({'name': item, 'size': size})

    # Sortierung: Größte Ordner zuerst (Erleichtert die Verteilung)
    items.sort(key=lambda x: x['size'], reverse=True)

    # Schritt 2: Verteilung auf die "virtuellen" Festplatten (Bin-Packing)
    disks = []

    for item in items:
        if item['size'] > MAX_DISK_SIZE:
            print(
                f"⚠️ WARNUNG: '{item['name']}' ({item['size'] / (1024 ** 3):.2f} GB) ist größer als eine einzelne Zielplatte!")
            continue

        # Suchen, ob der Ordner noch auf eine bereits angefangene Platte passt
        placed = False
        for disk in disks:
            if disk['current_size'] + item['size'] <= MAX_DISK_SIZE:
                disk['items'].append(item)
                disk['current_size'] += item['size']
                placed = True
                break

        # Wenn er nirgends reinpasst, machen wir eine neue Platte auf
        if not placed:
            disks.append({
                'current_size': item['size'],
                'items': [item]
            })

    # Schritt 3: Ergebnis ausgeben
    print("\n" + "=" * 40)
    print(f"BERECHNETE AUFTEILUNG (Zielgröße: {max_disk_size_gb} GB):")
    print("=" * 40)

    for idx, disk in enumerate(disks, 1):
        size_gb = disk['current_size'] / (1024 ** 3)
        print(f"\n💾 [Virtuelle Festplatte #{idx}] - Belegt: {size_gb:.2f} GB / {max_disk_size_gb} GB")
        print("-" * 50)
        for item in disk['items']:
            item_gb = item['size'] / (1024 ** 3)
            print(f"  ├── {item['name']} ({item_gb:.2f} GB)")

    return disks


# --- KONFIGURATION ---
QUELL_PFAD = "/path/to/your/big/media/collection"
PRO_PLATTE_GB = 3700  # Z.B. ~3.7 TB nutzbarer Platz auf einer 4TB-Platte (Sicherheitspuffer!)

if __name__ == "__main__":
    plan_backup_chunks(QUELL_PFAD, PRO_PLATTE_GB)