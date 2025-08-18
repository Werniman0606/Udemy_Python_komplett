import os
import time

# --- CONFIGURATION START ---
# Source directory where the script will start looking for files
SOURCE_DIR = r'd:\RedditDownload\reddit_sub_VintageSmut'

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

        # Get the name of the current folder
        folder_name = os.path.basename(root)

        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is an allowed image format
            if file.lower().endswith(ALLOWED_EXTENSIONS):
                # Check if the file is already renamed to prevent duplicates
                if not file.startswith(f'[{folder_name}]_'):

                    # Create the new file name
                    new_file_name = f'[{folder_name}]_{file}'
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

    print("\n---")
    print("Process complete.")
    print(f"Total {renamed_count} files renamed.")
    print(f"Duration: {duration:.2f} seconds")


if __name__ == '__main__':
    main()