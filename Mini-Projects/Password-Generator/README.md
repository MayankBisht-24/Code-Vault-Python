# 🔐 Password Generator

A secure command-line password generator built with Python.

This project generates cryptographically secure passwords based on user-defined preferences such as password length and character types. It validates user input, guarantees character diversity, and provides a simple password strength indicator.

---

## ✨ Features

- ✅ Generate passwords with a custom length (1–24 characters)
- ✅ Include uppercase letters
- ✅ Include lowercase letters
- ✅ Include numbers
- ✅ Include special characters
- ✅ Guarantees at least one character from every selected category
- ✅ Uses Python's `secrets` module for cryptographically secure randomness
- ✅ Password strength indicator
- ✅ Strict input validation
- ✅ Generate multiple passwords without restarting the program
- ✅ Beginner-friendly and well-structured code

---

## 🛠 Tech Stack

- Python 3
- `secrets`
- `string`

---

## 📂 Project Structure

```text
Password-Generator/
├── password_generator.py
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

Go to the project folder:

```bash
cd Code-Vault-Python/Mini-Projects/Password-Generator
```

Run the program:

```bash
python password_generator.py
```

---

## 💻 Example Output

```text
=== Password Generator ===

Password Length: 16

Include Uppercase? (Y/N): Y
Include Lowercase? (Y/N): Y
Include Numbers? (Y/N): Y
Include Symbols? (Y/N): Y

Generated Password:
A@8kLm#2Qx!7Pr$N

Strength:
██████████
Very Strong

Generate another password? (Y/N): N

Have a good day!
```

---

## 📚 Concepts Practiced

- Functions
- Loops
- Input Validation
- Constants
- String Manipulation
- Cryptographically Secure Randomness
- Fisher–Yates Shuffle
- Clean Code Practices
- Python Standard Library

---

## 🔮 Future Improvements

- Clipboard support
- Password history
- Save passwords to a file
- GUI version using Tkinter
- Web version using Flask
- Custom symbol selection
- Exclude confusing characters (O, 0, l, 1)

---

## 👨‍💻 Author

**Mayank Bisht**

GitHub:
https://github.com/MayankBisht-24