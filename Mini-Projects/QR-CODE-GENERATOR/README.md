<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c3e50,100:3498db&height=200&section=header&text=QR%20Code%20Generator&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=A%20Sleek,%20Menu-Driven%20CLI%20Tool%20for%20Every%20QR%20Need&descAlignY=55&descSize=18" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&duration=3000&pause=800&color=3498DB&center=true&vCenter=true&width=600&lines=Text+%E2%86%92+QR;URL+%E2%86%92+QR;Wi-Fi+%E2%86%92+QR;Email+%E2%86%92+QR;Anything+%E2%86%92+QR+%F0%9F%93%B1" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![qrcode](https://img.shields.io/badge/qrcode-8.2-2ecc71?style=for-the-badge)
![Pillow](https://img.shields.io/badge/Pillow-12.3-e74c3c?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=flat-square)
![Author](https://img.shields.io/badge/Author-Mayank%20Bisht-3498db?style=flat-square)

</div>

---

## 📖 Overview

**QR Code Generator** is a beginner-friendly yet feature-rich **command line tool**
written in Python that converts plain text, URLs, emails, phone numbers, Wi-Fi
credentials, and social media links into scannable QR codes — complete with
custom colors, transparent backgrounds, embedded logos, multiple export
formats, and bulk generation from a file.

It's built with clean, modular, well-documented code, making it just as
useful as a learning reference as it is as a practical tool.

<div align="center">
<img src="assets/example_qr.png" width="220" alt="Example QR Code"/>

<sub>👆 Scan me — this QR points to github.com</sub>
</div>

<br/>

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 📥 Input Types
- 📝 Plain Text
- 🔗 URLs / Websites
- 📧 Email (`mailto:` + subject/body)
- 📞 Phone Numbers (`tel:`)
- 📶 Wi-Fi Credentials (scan-to-connect)
- 📱 Social Media Links

</td>
<td width="50%" valign="top">

### 🎨 Customization
- 📏 Adjustable QR size & border
- 🛡️ 4 error-correction levels
- 🎨 Custom fill & background color
- 🌫️ Transparent background
- 🖼️ Center logo embedding
- 📄 Export as PNG / JPG / SVG

</td>
</tr>
</table>

### ✅ Validation & Error Handling

| Scenario | Behavior |
|---|---|
| Empty input | ❌ Rejected with a clear message |
| Invalid filename | ❌ Rejected — illegal characters flagged |
| Extra whitespace | 🧹 Automatically trimmed |
| `Ctrl + C` | 🛑 Caught gracefully, no ugly traceback |
| Closed input stream (`EOF`) | 🛑 Handled gracefully |
| `PermissionError` on save | ⚠️ Reported, no crash |
| Any unexpected exception | ⚠️ Caught and reported |

### 🌟 Bonus Features

| | | |
|---|---|---|
| ⭐ Colored QR Codes | ⭐ Custom Background Color | ⭐ Transparent Background |
| ⭐ Center Logo Embedding | ⭐ Bulk Generation from Text File | ⭐ Instant Preview |
| ⭐ SVG Export | ⭐ JPG Export | ⭐ Beginner-Friendly Code |

---

## 🖥️ User Menu

```
=========================
      QR Generator
=========================

1. Generate QR Code
2. Generate Multiple QR Codes from a Text File
3. Exit
```

## 📤 Sample Output

```
✅ QR Code Generated Successfully!

Saved At:

output/my_qr.png
```

<br/>

## 🛠 Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![qrcode](https://img.shields.io/badge/qrcode-2ecc71?style=flat-square&logoColor=white)
![Pillow](https://img.shields.io/badge/Pillow-e74c3c?style=flat-square&logoColor=white)

</div>

**Requirements:**
- Python 3.8+
- [`qrcode`](https://pypi.org/project/qrcode/)
- [`Pillow`](https://pypi.org/project/Pillow/)

## ⚙️ Installation

```bash
# 1. Clone or download this folder
cd Mini-Projects/QR-Code-Generator

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## ▶️ How to Run

```bash
python qr_code_generator.py
```

Follow the on-screen menu — choose what to encode, tweak size/color/format
if you like, and your QR code lands in the `output/` folder.

**Bulk mode:** pick option `2`, point it at a `.txt` file (one item per
line), and it'll generate `qr_1.png`, `qr_2.png`, etc. for every entry.

## 📂 Folder Structure

```
Mini-Projects/
└── QR-Code-Generator/
    ├── qr_code_generator.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    ├── output/          # generated QR codes land here
    └── assets/          # images used in this README
```

## 🧠 Concepts Practiced

- CLI menu design and input-loop control flow
- Input validation and defensive programming
- Exception handling (`ValueError`, `PermissionError`, `KeyboardInterrupt`, `EOFError`)
- String parsing & escaping (Wi-Fi QR payload per spec)
- Image manipulation with `Pillow` (resize, paste, RGBA/RGB conversion)
- File I/O and safe path/filename handling
- Writing modular, documented, beginner-friendly Python

---

## 🗺️ Roadmap

- [ ] Add a GUI version (Tkinter / PyQt)
- [ ] Batch export to a single PDF sheet
- [ ] Add QR code *scanning* / decoding support
- [ ] Dark-mode themed QR presets

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the **MIT License** — free to use, modify,
and distribute.

---

## 👨‍💻 Author

<div align="center">

<img src="https://img.shields.io/badge/Author-Mayank%20Bisht-3498db?style=for-the-badge&logo=github&logoColor=white"/>

**Mayank Bisht**
*BCA Student — Data Science Specialization*

Built with 💙, patience, and a healthy amount of `Ctrl+C` debugging.

</div>

<div align="center">

### ⭐ If this project helped you, consider giving it a star!

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3498db,100:2c3e50&height=100&section=footer" width="100%"/>

</div>