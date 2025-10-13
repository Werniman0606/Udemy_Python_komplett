import os
import time

# --- CONFIGURATION START ---
# Source directory where the script will start looking for files
SOURCE_DIR = r'e:\Bilder\Celebrities'

# Allowed image formats
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')


# --- CONFIGURATION END ---

def main():
    print("Starting the file renaming process...")
    print(f"Searching for images in: '{SOURCE_DIR}'")

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Error: Source directory '{SOURCE_DIR}' not found.")
        return

    renamed_count = 0
    start_time = time.time()

    # Walk through the source directory and its subdirectories
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Exclude the base directory itself
        if root == SOURCE_DIR:
            continue

        # Get the name of the current folder, e.g., "Beatrice Egli"
        folder_name = os.path.basename(root)

        # Das benötigte Präfix in der gewünschten Form, z.B. "[Beatrice Egli]_"
        required_prefix = f'[{folder_name}]_'

        for file in files:
            # Check if the file is an allowed image format
            if file.lower().endswith(ALLOWED_EXTENSIONS):

                # *** WICHTIGE ANPASSUNG HIER ***
                # Prüfen, ob der Dateiname BEREITS mit dem benötigten Präfix beginnt
                if file.startswith(required_prefix):
                    print(f"➡️ Skipping: '{file}' (Already correctly named)")
                    continue  # Springe zur nächsten Datei
                # *******************************

                file_path = os.path.join(root, file)

                # Create the new file name
                new_file_name = f'{required_prefix}{file}'
                new_file_path = os.path.join(root, new_file_name)

                try:
                    os.rename(file_path, new_file_path)
                    print(f"✅ Renamed: '{file}' -> '{new_file_name}'")
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ Error renaming '{file}': {e}")
            else:
                print(f"➡️ Skipping non-image file: '{file}'")

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 50)
    print("Process complete.")
    print(f"Total {renamed_count} files renamed.")
    print(f"Duration: {duration:.2f} seconds")
    print("=" * 50)


if __name__ == '__main__':
    main()