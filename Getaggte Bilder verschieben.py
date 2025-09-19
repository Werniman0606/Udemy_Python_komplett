import os
import subprocess
import shutil
import time

# --- CONFIGURATION START ---
# Path to exiftool
EXIFTOOL_PATH = r'd:\exiftool-13.33_64\exiftool-13.33_64\exiftool.exe'

# Base directory to search for images
SOURCE_DIR = r'e:\Bilder\Celebrities\C\Chloe Morgane'

# Destination directory for tagged files
DEST_DIR = r'e:\Bilder-getaggt\Celebrities\C\Chloe Morgane'

# Allowed image formats
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


# --- CONFIGURATION END ---

def get_tag_counts(file_path):
    """
    Counts the number of face regions and person tags using a new, robust method.
    """
    try:
        # Use -T and specify all relevant tags. Add -r to find all tags.
        command = f'chcp 65001 & "{EXIFTOOL_PATH}" -T -XMP:RegionList -MP:RegionList -XMP-mwg-rs:Regions -XMP-acdsee-rs:ACDSeeRegionName -XMP-dc:creator "{file_path}"'

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            check=False,
            encoding='utf-8',
            errors='ignore'
        )

        output_list = result.stdout.strip().split('\t')

        region_count = 0
        creator_count = 0

        # Output columns are now fixed: RegionList, MP:RegionList, MWG-Regions, ACDSeeRegionName, Creator
        regions_output_mwg = output_list[2]
        regions_output_acdsee = output_list[3]
        creators_output = output_list[4]

        if regions_output_mwg and regions_output_mwg != '-':
            region_count += regions_output_mwg.count('{')

        if regions_output_acdsee and regions_output_acdsee != '-':
            region_count += regions_output_acdsee.count(',') + 1

        if creators_output and creators_output != '-':
            creator_count = creators_output.count(',') + 1

        return region_count, creator_count

    except Exception as e:
        print(f"⚠️ Error reading tags for {file_path}: {e}")
        return 0, 0


def move_file(source_path, dest_base_dir):
    """
    Moves a file while preserving its original directory structure.
    """
    relative_path = os.path.relpath(source_path, SOURCE_DIR)
    dest_path = os.path.join(dest_base_dir, relative_path)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    try:
        shutil.move(source_path, dest_path)
        return True
    except Exception as e:
        print(f"❌ Error moving '{source_path}' to '{dest_path}': {e}")
        return False


def main():
    print("Starting the move process for fully tagged images...")
    print(f"Searching for images in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Error: Source directory '{SOURCE_DIR}' not found.")
        return

    if not os.path.exists(DEST_DIR):
        print(f"⚠️ Destination directory '{DEST_DIR}' does not exist. Creating it now.")
        os.makedirs(DEST_DIR, exist_ok=True)

    moved_count = 0
    start_time = time.time()

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)

            if file.lower().endswith(ALLOWED_EXTENSIONS):
                region_count, creator_count = get_tag_counts(file_path)

                if creator_count > 0 and region_count == creator_count:
                    if move_file(file_path, DEST_DIR):
                        print(
                            f"✅ Moved: {file_path} -> {os.path.join(DEST_DIR, os.path.relpath(file_path, SOURCE_DIR))}")
                        moved_count += 1
                else:
                    print(f"➡️ Skipping: {file_path} (Regions: {region_count}, Tags: {creator_count})")

    end_time = time.time()
    duration = end_time - start_time

    print("\n---")
    print("Process complete.")
    print(f"Total {moved_count} files moved.")
    print(f"Duration: {duration:.2f} seconds")


if __name__ == '__main__':
    main()