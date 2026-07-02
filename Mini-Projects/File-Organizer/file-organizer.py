"""
File Organizer
--------------
A simple command-line tool that organizes files inside a folder into
category-based subfolders (Images, Documents, Videos, Audio, Archives,
Executables, Others) based on their file extensions.

Modules used: os, shutil, pathlib
"""

import os
import shutil
from pathlib import Path


# Mapping of category name -> list of file extensions that belong to it.
# Using a dictionary makes it easy to add/remove categories later.
FILE_CATEGORIES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"],
    "Executables": [".exe", ".msi"],
    "Others": [],  # fallback category for anything that doesn't match above
}


def get_category(file_extension):
    """
    Determine which category a file belongs to, based on its extension.

    Args:
        file_extension (str): The file extension, e.g. ".jpg"

    Returns:
        str: The matching category name, or "Others" if no match is found.
    """
    file_extension = file_extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if file_extension in extensions:
            return category

    return "Others"


def create_folder(folder_path):
    """
    Create a folder at the given path if it does not already exist.

    Args:
        folder_path (Path): Path of the folder to create.

    Returns:
        bool: True if a new folder was created, False if it already existed.
    """
    path = Path(folder_path)

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Folder created: {path}")
        return True

    return False


def move_file(file_path, destination_folder):
    """
    Move a single file into the destination folder.

    Handles common errors (permission issues, duplicate file names)
    without crashing the whole program.

    Args:
        file_path (Path): Path of the file to move.
        destination_folder (Path): Folder the file should be moved into.

    Returns:
        bool: True if the file was moved successfully, False otherwise.
    """
    try:
        destination_path = Path(destination_folder) / file_path.name

        # If a file with the same name already exists at the destination,
        # rename the incoming file instead of overwriting it.
        if destination_path.exists():
            base_name = file_path.stem
            extension = file_path.suffix
            counter = 1

            while destination_path.exists():
                new_name = f"{base_name}_{counter}{extension}"
                destination_path = Path(destination_folder) / new_name
                counter += 1

        shutil.move(str(file_path), str(destination_path))
        print(f"File moved: {file_path.name} -> {destination_folder.name}/")
        return True

    except PermissionError:
        print(f"Permission denied: could not move '{file_path.name}'")
        return False

    except Exception as error:
        print(f"Could not move '{file_path.name}': {error}")
        return False


def organize_folder(folder_path):
    """
    Organize all files inside the given folder into category subfolders.

    Args:
        folder_path (Path): The folder whose files should be organized.

    Returns:
        int: Total number of files successfully organized.
    """
    folder_path = Path(folder_path)
    files_organized = 0

    for item in folder_path.iterdir():

        # Skip subfolders entirely; we only organize files.
        if item.is_dir():
            continue

        category = get_category(item.suffix)
        category_folder = folder_path / category

        create_folder(category_folder)

        if move_file(item, category_folder):
            files_organized += 1

    return files_organized


def main():
    """
    Entry point of the program. Takes user input, validates it,
    runs the organizer, and prints a summary.
    """
    folder_input = input("Enter folder path: ").strip()
    folder_path = Path(folder_input)

    # --- Validation ---
    if not folder_path.exists():
        print("Error: This folder path does not exist.")
        return

    if not folder_path.is_dir():
        print("Error: The given path is not a folder.")
        return

    try:
        total_files = organize_folder(folder_path)
        print(f"\nTotal files organized: {total_files}")

    except PermissionError:
        print("Error: Permission denied while accessing the folder.")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()