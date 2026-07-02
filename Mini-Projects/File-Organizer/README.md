# 📂 File Organizer

A Python command-line utility that automatically organizes files into category-based folders according to their file extensions.

This project helps keep directories clean by sorting files into organized folders while safely handling duplicate filenames, invalid paths, and common file system errors.

---

## ✨ Features

- ✅ Automatically organizes files by extension
- ✅ Creates category folders if they don't already exist
- ✅ Supports Images, Documents, Videos, Audio, Archives, Executables, and Others
- ✅ Prevents overwriting duplicate files by automatically renaming them
- ✅ Skips existing folders and organizes only files
- ✅ Handles invalid folder paths gracefully
- ✅ Handles permission errors without crashing
- ✅ Displays the total number of files organized
- ✅ Clean, modular, and beginner-friendly code

---

## 🛠 Tech Stack

- Python 3
- `os`
- `shutil`
- `pathlib`

---

## 📂 Project Structure

```text
File-Organizer/
├── file_organizer.py
└── README.md
```

---

## 🚀 Getting Started

### Requirements

- Python 3.6 or later

No external libraries are required.

---

### Installation

Clone the repository:

```bash
git clone https://github.com/MayankBisht-24/Code-Vault-Python.git
```

Navigate to the project directory:

```bash
cd Code-Vault-Python/Mini-Projects/File-Organizer
```

Run the program:

```bash
python file_organizer.py
```

---

## 💻 Example Output

```text
Enter folder path:

D:\Downloads

Folder created: Images
Folder created: Documents
Folder created: Archives

File moved: photo.jpg -> Images/
File moved: report.pdf -> Documents/
File moved: music.mp3 -> Audio/
File moved: project.zip -> Archives/

Total files organized: 12
```

---

## 📁 Supported File Types

| Category | Extensions |
|----------|------------|
| Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp` |
| Documents | `.pdf`, `.docx`, `.txt`, `.pptx`, `.xlsx` |
| Videos | `.mp4`, `.mkv`, `.mov` |
| Audio | `.mp3`, `.wav` |
| Archives | `.zip`, `.rar` |
| Executables | `.exe`, `.msi` |
| Others | Any unsupported file type |

---

## 📚 Concepts Practiced

- Functions
- Loops
- Dictionaries
- Conditional Statements
- Exception Handling
- File Handling
- Path Manipulation
- `os` Module
- `shutil` Module
- `pathlib` Module
- Clean Code Practices

---

## 👨‍💻 Author

**Mayank Bisht**

GitHub:
https://github.com/MayankBisht-24