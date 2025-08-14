import os
import shutil

# This script renames image files in a directory and its subdirectories.
# It prefixes the filename with the name of its parent folder in square brackets.

def rename_images_with_folder_name(base_path):
    """
    Renames image files in a specified directory and all its subdirectories.

    Args:
        base_path (str): The absolute path of the directory to start the renaming process.
    """
    if not os.path.isdir(base_path):
        print(f"Fehler: Der Basispfad '{base_path}' existiert nicht oder ist kein Verzeichnis.")
        return

    print(f"Starte Umbenennungsvorgang im Basispfad: {base_path}\n")

    # Tuple of allowed image file extensions (case-insensitive)
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.avif')

    # Use os.walk to iterate through all directories and files
    for root, _, files in os.walk(base_path):
        # Extract the name of the parent folder
        parent_folder_name = os.path.basename(root)

        for filename in files:
            # Check if the file is an image
            if filename.lower().endswith(image_extensions):
                # Wenn der Dateiname bereits mit einer öffnenden eckigen Klammer beginnt,
                # wird er übersprungen.
                if filename.startswith('['):
                    print(f"  Überspringe '{filename}' (bereits getaggt oder umbenannt).")
                    continue

                old_file_path = os.path.join(root, filename)

                # Split the filename to get name and extension
                name, extension = os.path.splitext(filename)

                # Construct the new filename
                # Example: [Bonnie Tyler]_1.jpg
                new_filename = f"[{parent_folder_name}]_{name}{extension}"
                new_file_path = os.path.join(root, new_filename)

                try:
                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    print(f"  Umbenannt: '{filename}' -> '{new_filename}'")
                except OSError as e:
                    print(f"  Fehler beim Umbenennen von '{filename}': {e}")
            else:
                print(f"  Überspringe '{filename}' (kein Bildformat).")

    print("\nUmbenennungsvorgang abgeschlossen.")

# --- Script usage ---
if __name__ == "__main__":
    # Define the base directory.
    # IMPORTANT: Use a "raw string" (r'...') to avoid issues with backslashes.
    base_directory = r'/run/media/marco/Laufwerk D/RedditDownload/reddit_sub_VintageSmut'

    # A complete backup of your files is strongly recommended before running any script that modifies them.
    # It's also a good idea to first test the script on a small, dedicated test folder.
    rename_images_with_folder_name(base_directory)