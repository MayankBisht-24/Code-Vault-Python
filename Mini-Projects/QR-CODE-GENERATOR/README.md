# 📱 QR Code Generator (CLI)

A beginner-friendly, menu-driven **command line QR code generator** built in Python.
Turn plain text, URLs, emails, phone numbers, Wi-Fi credentials, and social links
into scannable QR codes — with custom colors, transparent backgrounds, logos,
multiple export formats, and bulk generation from a file.

![Example QR Code](assets/example_qr.png)

---

## ✨ Features

### 📥 Input
- Plain text
- URLs / websites
- Email addresses (`mailto:` with optional subject & body)
- Phone numbers (`tel:` format)
- Wi-Fi credentials (auto-generates a scan-to-connect QR)
- Social media links

### ✅ Validation
- Empty input is rejected
- Invalid filenames (illegal characters) are rejected
- Extra whitespace is trimmed automatically
- Graceful handling of `Ctrl + C` (KeyboardInterrupt) and closed input streams

### 🧩 QR Generation
- Generate a single QR code, or many at once from a text file
- Save as **PNG**, **JPG**, or **SVG**
- Custom filename, with a sensible default (`qr_code.png`) if left blank
- Auto-creates the `output/` folder if it doesn't exist

### 🎨 Image Customization
- Adjustable QR size (box size)
- Adjustable border/quiet-zone size
- Selectable error-correction level: Low, Medium, Quartile, High
- Custom fill color and background color (named colors like `blue`, or hex like `#3498db`)
- Transparent background option
- Add a logo image to the center of the QR code

### 🖥️ User Menu
```
=========================
      QR Generator
=========================

1. Generate QR Code
2. Generate Multiple QR Codes from a Text File
3. Exit
```

### 📤 Output
```
✅ QR Code Generated Successfully!

Saved At:

output/my_qr.png
```

### 🛡️ Error Handling
- Invalid input (empty fields, bad emails/phone numbers)
- Invalid filenames
- `PermissionError` when saving is blocked
- `KeyboardInterrupt` (Ctrl+C) at any point
- Any other unexpected exception, caught and reported without crashing

---

## 🛠 Requirements
- Python 3.8+
- [`qrcode`](https://pypi.org/project/qrcode/)
- [`Pillow`](https://pypi.org/project/Pillow/)

---

## ⚙️ Installation

```bash
# 1. Clone or download this folder
cd Mini-Projects/QR-Code-Generator

# 2. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python qr_code_generator.py
```

Then just follow the on-screen menu — pick what you want to encode, tweak
the size/color/format if you like, and your QR code lands in the `output/`
folder.

**Bulk mode:** choose option `2` from the main menu and point it at a `.txt`
file with one item per line (URLs, text, whatever) — it'll generate
`qr_1.png`, `qr_2.png`, etc. for every non-empty line.

---

## 📂 Folder Structure

```
Mini-Projects/
└── QR-Code-Generator/
    ├── qr_code_generator.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    ├── output/          # generated QR codes land here
    └── assets/          # example images used in this README
```

---

## 🖼️ Example Output

Input: `https://github.com/`
Options: box size `10`, border `4`, error correction `High`, fill color `#2c3e50`

```
output/example_qr.png
```

![Example QR Code](assets/example_qr.png)

---

## 🧠 Concepts Practiced
- CLI menu design and input-loop control flow
- Input validation and defensive programming
- Custom exceptions vs. built-in exception handling (`ValueError`, `PermissionError`, `KeyboardInterrupt`, `EOFError`)
- String parsing & escaping (building the Wi-Fi QR payload per spec)
- Working with the `qrcode` and `Pillow` libraries
- Image manipulation (resizing, pasting, RGBA/RGB conversion for logos & transparency)
- File I/O and safe path/filename handling
- Writing modular, documented, beginner-friendly Python (constants, functions, docstrings)

---

## 🌟 Bonus Features
- ⭐ Colored QR codes (custom fill color)
- ⭐ Custom background color
- ⭐ Transparent background
- ⭐ Add a logo in the center
- ⭐ Generate multiple QR codes from a text file
- ⭐ Preview the QR code right after generation
- ⭐ Export as SVG
- ⭐ Export as JPG

---

## 📌 Notes
- For Wi-Fi QR codes, most phone cameras can scan the code and offer a
  "Connect to Wi-Fi" prompt directly — no typing the password needed.
- SVG output can't be opened with the built-in preview (no default image
  viewer opens vector files) — open it in a browser or vector editor instead.
- JPG doesn't support transparency, so a transparent QR saved as `.jpg`
  will automatically be flattened onto a white background.