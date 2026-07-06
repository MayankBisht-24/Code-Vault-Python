"""
Duplicate File Finder
----------------------
A simple command-line tool that scans a folder (including all its
sub-folders) and finds files that are exact duplicates of one another,
based on their actual content rather than their file name.

How it works:
    Every file is read in small chunks and passed through the SHA-256
    hashing algorithm. Two files that produce the same hash are
    guaranteed (for all practical purposes) to have identical content.
    Files are then grouped by their hash, and any group with more than
    one file is reported as a duplicate group.
"""

import os
import sys
from pathlib import Path
import hashlib
from collections import defaultdict

# Number of bytes read from a file at a time.
# Reading in chunks keeps memory usage low even for very large files.
CHUNK_SIZE = 4096


def get_folder_path():
    """
    Ask the user for a folder path and make sure it is actually usable
    before we try to scan it.

    Returns:
        Path: A validated Path object pointing to an existing directory.
    """
    while True:
        raw_input_path = input("Enter the folder path to scan: ").strip()

        if not raw_input_path:
            print("Error: Folder path cannot be empty. Please try again.\n")
            continue

        folder_path = Path(raw_input_path)

        if not folder_path.exists():
            print(f"Error: The path '{folder_path}' does not exist. Please try again.\n")
            continue

        if not folder_path.is_dir():
            print(f"Error: '{folder_path}' is not a folder. Please try again.\n")
            continue

        return folder_path


def calculate_hash(file_path, chunk_size=CHUNK_SIZE):
    """
    Calculate the SHA-256 hash of a file by reading it in small chunks,
    instead of loading the whole file into memory at once.

    Args:
        file_path (Path): Path to the file to hash.
        chunk_size (int): Number of bytes to read per chunk.

    Returns:
        str or None: The hex digest of the file, or None if the file
        could not be read (e.g. permission denied).
    """
    sha256_hash = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()

    except PermissionError:
        print(f"Warning: Permission denied while reading '{file_path}'. Skipping this file.")
        return None
    except (OSError, IOError) as error:
        print(f"Warning: Could not read '{file_path}' ({error}). Skipping this file.")
        return None


def format_size(size_in_bytes):
    """
    Convert a raw byte count into a human-readable string using
    the most appropriate unit (B, KB, or MB).

    Args:
        size_in_bytes (int): File size in bytes.

    Returns:
        str: Formatted size, e.g. "245.30 KB" or "1.75 MB".
    """
    kb = size_in_bytes / 1024
    mb = kb / 1024

    if mb >= 1:
        return f"{mb:.2f} MB"
    elif kb >= 1:
        return f"{kb:.2f} KB"
    else:
        return f"{size_in_bytes} B"


def find_duplicates(folder_path):
    """
    Recursively scan the given folder and group files by content hash.

    Args:
        folder_path (Path): The root folder to scan.

    Returns:
        tuple: (duplicates, stats) where
            duplicates is a dict mapping hash -> list of file paths
                       (only for hashes that have more than one file),
            stats is a dict with counts of folders scanned, files
                       scanned, and any files that were skipped.
    """
    hash_map = defaultdict(list)

    folders_scanned = 0
    files_scanned = 0
    files_skipped = 0

    for current_root, sub_dirs, file_names in os.walk(folder_path):
        folders_scanned += 1

        for file_name in file_names:
            file_path = Path(current_root) / file_name

            # Skip broken symlinks or files that vanish mid-scan.
            if not file_path.is_file():
                continue

            file_hash = calculate_hash(file_path)

            if file_hash is None:
                files_skipped += 1
                continue

            hash_map[file_hash].append(file_path)
            files_scanned += 1

    # Keep only the groups that actually have more than one file in them.
    duplicates = {
        file_hash: paths
        for file_hash, paths in hash_map.items()
        if len(paths) > 1
    }

    stats = {
        "folders_scanned": folders_scanned,
        "files_scanned": files_scanned,
        "files_skipped": files_skipped,
    }

    return duplicates, stats


def display_duplicates(duplicates, stats):
    """
    Print the duplicate groups and the final summary in a clean,
    easy-to-read format.

    Args:
        duplicates (dict): hash -> list of duplicate file paths.
        stats (dict): Scan statistics from find_duplicates().
    """
    if not duplicates:
        print("\nNo duplicate files were found. Your folder is squeaky clean!\n")
    else:
        total_duplicate_files = 0

        for group_number, (file_hash, file_paths) in enumerate(duplicates.items(), start=1):
            print(f"\nDuplicate Group #{group_number}")

            # The first file found is treated as the "original";
            # everything after it in the group is a duplicate copy.
            original_path = file_paths[0]
            file_size = format_size(original_path.stat().st_size)

            print(f"File Size: {file_size}")
            print("\nOriginal:")
            print(original_path)

            print("\nDuplicate(s):")
            for duplicate_path in file_paths[1:]:
                print(duplicate_path)
                total_duplicate_files += 1

            print("-" * 40)

    print("\n" + "=" * 40)
    print("Summary")
    print("=" * 40)
    print(f"Folders Scanned  : {stats['folders_scanned']}")
    print(f"Files Scanned    : {stats['files_scanned']}")
    print(f"Duplicate Groups : {len(duplicates)}")
    print(f"Duplicate Files  : {sum(len(paths) - 1 for paths in duplicates.values())}")

    if stats["files_skipped"] > 0:
        print(f"Files Skipped    : {stats['files_skipped']} (permission/access errors)")

    print("=" * 40 + "\n")


def main():
    """
    Entry point of the program. Ties everything together and handles
    the errors that could realistically happen during a real scan.
    """
    print("=" * 40)
    print("      Duplicate File Finder")
    print("=" * 40)

    try:
        folder_path = get_folder_path()

        print("\nScanning... this might take a moment for large folders.\n")

        duplicates, stats = find_duplicates(folder_path)
        display_duplicates(duplicates, stats)

    except KeyboardInterrupt:
        print("\n\nScan cancelled by user. Exiting gracefully.")
        sys.exit(0)

    except Exception as unexpected_error:
        print(f"\nAn unexpected error occurred: {unexpected_error}")
        sys.exit(1)


if __name__ == "__main__":
    main()