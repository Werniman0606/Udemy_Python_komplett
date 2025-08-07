import os
import shutil
import re

source_directory = r'E:\Bilder\Sexbilder'
destination_directory = r'D:\extracted\Test'

# Create the destination folder if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# Regex to find a year between 1920 and 2000, preceded by a space and followed by a hyphen
# The '\b' ensures that the year is a whole word
pattern = re.compile(r' 19[2-9]\d|2000-')

for filename in os.listdir(source_directory):
    if pattern.search(filename):
        source_path = os.path.join(source_directory, filename)
        destination_path = os.path.join(destination_directory, filename)

        # Check if the file is a regular file before moving
        if os.path.isfile(source_path):
            try:
                shutil.move(source_path, destination_path)
                print(f"Moved: {filename}")
            except Exception as e:
                print(f"Error moving {filename}: {e}")