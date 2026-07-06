# Duplicate File Finder (CLI)

A simple Python command-line tool that scans a folder — and all of its
sub-folders — to find files that are exact duplicates of each other,
based on their **content**, not their file name.

## Why content-based comparison?

Two files can have completely different names but identical content
(for example, `image.jpg` and `image_copy.jpg`). This tool uses the
**SHA-256** hashing algorithm to fingerprint each file's actual data,
so it correctly identifies duplicates even when names don't match, and
correctly ignores files that happen to share a name but hold different
content.

## Features

- Recursively scans a folder and all its sub-folders
- Detects duplicates using SHA-256 content hashing
- Reads files in small chunks (4096 bytes) so even large files don't
  get loaded fully into memory
- Displays the file size of each duplicate group (in B / KB / MB)
- Shows a clear summary: folders scanned, files scanned, duplicate
  groups, and total duplicate files
- Handles common real-world errors gracefully:
  - Empty input
  - Invalid or missing folder path
  - Permission denied
  - File access errors
  - Manual interruption (`Ctrl + C`)

## Requirements

None. This project only uses Python's standard library
(`os`, `pathlib`, `hashlib`, `collections`).

Python 3.7 or newer is recommended.

## Usage

```bash
python duplicate_file_finder.py
```

You'll be prompted to enter a folder path:

```
Enter the folder path to scan: D:\Photos
```

The tool will then scan the folder and print out any duplicate groups
it finds, along with a summary.

## Example Output

```
========================================
      Duplicate File Finder
========================================
Enter the folder path to scan: D:\Photos

Scanning... this might take a moment for large folders.

Duplicate Group #1
File Size: 245.30 KB

Original:
D:\Photos\image.jpg

Duplicate(s):
D:\Backup\image_copy.jpg
----------------------------------------

========================================
Summary
========================================
Folders Scanned  : 12
Files Scanned    : 148
Duplicate Groups  : 1
Duplicate Files  : 1
========================================
```

## Project Structure

```
Duplicate-File-Finder/
├── duplicate_file_finder.py   # Main script
├── README.md                  # Project documentation
├── requirements.txt           # Dependencies (none, standard library only)
└── .gitignore                 # Files/folders excluded from git
```

## How It Works (Under the Hood)

1. **`get_folder_path()`** — asks the user for a folder path and keeps
   asking until a valid, existing directory is provided.
2. **`calculate_hash()`** — reads a file in small chunks and computes
   its SHA-256 hash, so memory usage stays low regardless of file size.
3. **`find_duplicates()`** — walks through the folder tree, hashes
   every file, and groups files that share the same hash.
4. **`format_size()`** — converts a raw byte count into a readable
   B / KB / MB string.
5. **`display_duplicates()`** — prints the duplicate groups along with
   file sizes, and a final summary of the scan.
6. **`main()`** — coordinates everything and catches errors like
   permission issues or a manual `Ctrl + C` interruption.

## Possible Future Improvements

- Option to automatically delete or move duplicate files
- Export results to a CSV or text report
- Multi-threaded hashing for faster scans on large folders
- Filter by file type or minimum file size

## License

Feel free to use, modify, and share this project for learning purposes.