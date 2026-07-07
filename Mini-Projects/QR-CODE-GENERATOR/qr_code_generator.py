"""
QR Code Generator (CLI)
=======================

A beginner-friendly, menu-driven command line tool that turns text, URLs,
emails, phone numbers, Wi-Fi credentials, and social media links into QR
codes. Supports custom colors, transparent backgrounds, logos in the
center, PNG/JPG/SVG export, bulk generation from a text file, and an
optional preview after generation.

Run it with:
    python qr_code_generator.py
"""

import os
import re
import sys
import string

import qrcode
import qrcode.image.svg
from qrcode.constants import (
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H,
)
from PIL import Image


# --------------------------------------------------------------------------- #
# Constants
# --------------------------------------------------------------------------- #

OUTPUT_DIR = "output"
DEFAULT_FILENAME = "qr_code"
VALID_EXTENSIONS = (".png", ".jpg", ".jpeg", ".svg")

ERROR_CORRECTION_LEVELS = {
    "1": ("Low", ERROR_CORRECT_L),
    "2": ("Medium", ERROR_CORRECT_M),
    "3": ("Quartile", ERROR_CORRECT_Q),
    "4": ("High", ERROR_CORRECT_H),
}

CONTENT_TYPES = {
    "1": "Plain Text",
    "2": "URL / Website",
    "3": "Email Address",
    "4": "Phone Number",
    "5": "Wi-Fi Credentials",
    "6": "Social Media Link",
}

# Characters that are unsafe inside a filename on most operating systems.
INVALID_FILENAME_CHARS = r'<>:"/\|?*'

# A handful of friendly named colors so users don't need to know hex codes.
NAMED_COLORS = {
    "black": "#000000",
    "white": "#ffffff",
    "red": "#e74c3c",
    "green": "#2ecc71",
    "blue": "#3498db",
    "yellow": "#f1c40f",
    "purple": "#9b59b6",
    "orange": "#e67e22",
    "pink": "#ff6fa5",
    "cyan": "#1abc9c",
}


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #

def print_banner() -> None:
    """Print the app title banner."""
    print("\n=========================")
    print("      QR Generator")
    print("=========================")


def print_menu() -> None:
    """Print the main menu options."""
    print("\n1. Generate QR Code")
    print("2. Generate Multiple QR Codes from a Text File")
    print("3. Exit")


def prompt(message: str) -> str:
    """
    Wrap input() so every prompt in the app trims whitespace consistently.
    Centralizing this makes it easy to add logging or i18n later.
    """
    return input(message).strip()


def ensure_output_dir() -> str:
    """Create the output/ folder if it doesn't already exist and return its path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return OUTPUT_DIR


def is_valid_filename(filename: str) -> bool:
    """Return True if filename has no illegal characters and isn't empty."""
    if not filename:
        return False
    if any(char in INVALID_FILENAME_CHARS for char in filename):
        return False
    if filename in {".", ".."}:
        return False
    return True


def resolve_filename(raw_name: str, file_format: str) -> str:
    """
    Turn user input into a safe filename with the correct extension.
    Falls back to DEFAULT_FILENAME if the user leaves it blank.
    """
    raw_name = raw_name.strip()
    extension = f".{file_format.lower()}"

    if not raw_name:
        return DEFAULT_FILENAME + extension

    # Strip any extension the user typed themselves; we control it based
    # on the format they picked, so duplicates like "qr.png.png" can't happen.
    for ext in VALID_EXTENSIONS:
        if raw_name.lower().endswith(ext):
            raw_name = raw_name[: -len(ext)]
            break

    if not is_valid_filename(raw_name):
        raise ValueError(
            f"Invalid filename '{raw_name}'. Avoid these characters: {INVALID_FILENAME_CHARS}"
        )

    return raw_name + extension


def resolve_color(raw_color: str, default: str) -> str:
    """Accept a named color (e.g. 'blue') or a raw hex code (e.g. '#3498db')."""
    raw_color = raw_color.strip().lower()
    if not raw_color:
        return default
    if raw_color in NAMED_COLORS:
        return NAMED_COLORS[raw_color]
    if re.fullmatch(r"#?[0-9a-f]{6}", raw_color):
        return raw_color if raw_color.startswith("#") else f"#{raw_color}"
    print(f"⚠️  Couldn't recognize color '{raw_color}', using default '{default}' instead.")
    return default


# --------------------------------------------------------------------------- #
# Content builders — turn the user's answers into the string a QR code holds
# --------------------------------------------------------------------------- #

def build_email_payload() -> str:
    """Prompt for an email address and return a mailto: QR payload."""
    email = prompt("Enter email address: ")
    if not email or "@" not in email:
        raise ValueError("A valid email address is required (must contain '@').")
    subject = prompt("Subject (optional, press Enter to skip): ")
    body = prompt("Body (optional, press Enter to skip): ")

    payload = f"mailto:{email}"
    params = []
    if subject:
        params.append(f"subject={subject}")
    if body:
        params.append(f"body={body}")
    if params:
        payload += "?" + "&".join(params)
    return payload


def build_phone_payload() -> str:
    """Prompt for a phone number and return a tel: QR payload."""
    phone = prompt("Enter phone number (with country code, e.g. +911234567890): ")
    cleaned = re.sub(r"[^\d+]", "", phone)
    if not cleaned or len(cleaned.replace("+", "")) < 7:
        raise ValueError("Please enter a valid phone number.")
    return f"tel:{cleaned}"


def build_wifi_payload() -> str:
    """Prompt for Wi-Fi credentials and return a standard WIFI: QR payload."""
    ssid = prompt("Wi-Fi Network Name (SSID): ")
    if not ssid:
        raise ValueError("SSID cannot be empty.")

    print("Security type: 1. WPA/WPA2   2. WEP   3. None")
    security_choice = prompt("Choose (1-3): ")
    security_map = {"1": "WPA", "2": "WEP", "3": "nopass"}
    security = security_map.get(security_choice, "WPA")

    password = ""
    if security != "nopass":
        password = prompt("Wi-Fi Password: ")
        if not password:
            raise ValueError("Password cannot be empty for a secured network.")

    hidden = prompt("Is this a hidden network? (y/N): ").lower() == "y"

    # Escape characters that are special in the WIFI QR spec.
    def escape(value: str) -> str:
        return re.sub(r"([\\;,:\"])", r"\\\1", value)

    payload = f"WIFI:T:{security};S:{escape(ssid)};"
    if password:
        payload += f"P:{escape(password)};"
    payload += f"H:{'true' if hidden else 'false'};;"
    return payload


def build_url_payload(is_social: bool = False) -> str:
    """Prompt for a URL / social link and normalize it with a scheme."""
    label = "social media link" if is_social else "URL"
    url = prompt(f"Enter {label}: ")
    if not url:
        raise ValueError(f"The {label} cannot be empty.")
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", url):
        url = "https://" + url
    return url


def build_text_payload() -> str:
    """Prompt for freeform plain text."""
    text = prompt("Enter the text you want to encode: ")
    if not text:
        raise ValueError("Text cannot be empty.")
    return text


def collect_qr_data() -> str:
    """Show the content-type submenu and dispatch to the right builder."""
    print("\nWhat would you like to encode?")
    for key, label in CONTENT_TYPES.items():
        print(f"{key}. {label}")

    choice = prompt("Choose an option: ")
    builders = {
        "1": build_text_payload,
        "2": lambda: build_url_payload(is_social=False),
        "3": build_email_payload,
        "4": build_phone_payload,
        "5": build_wifi_payload,
        "6": lambda: build_url_payload(is_social=True),
    }

    builder = builders.get(choice)
    if builder is None:
        raise ValueError("Invalid content type selection.")
    return builder()


# --------------------------------------------------------------------------- #
# QR image customization
# --------------------------------------------------------------------------- #

def choose_int(message: str, default: int, minimum: int = 1, maximum: int = 100) -> int:
    """Ask for an integer with a default, re-prompting on bad input."""
    raw = prompt(f"{message} (default {default}): ")
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        print(f"⚠️  Not a number, using default ({default}).")
        return default
    if not (minimum <= value <= maximum):
        print(f"⚠️  Out of range [{minimum}-{maximum}], using default ({default}).")
        return default
    return value


def choose_error_correction() -> int:
    """Show the error-correction submenu and return the qrcode constant."""
    print("\nError Correction Level:")
    for key, (name, _) in ERROR_CORRECTION_LEVELS.items():
        print(f"{key}. {name}")
    choice = prompt("Choose (default 2 - Medium): ") or "2"
    name, level = ERROR_CORRECTION_LEVELS.get(choice, ERROR_CORRECTION_LEVELS["2"])
    print(f"→ Using {name} error correction.")
    return level


def choose_file_format() -> str:
    """Ask which export format to use: PNG, JPG, or SVG."""
    print("\nExport Format: 1. PNG   2. JPG   3. SVG")
    choice = prompt("Choose (default 1 - PNG): ") or "1"
    return {"1": "png", "2": "jpg", "3": "svg"}.get(choice, "png")


def choose_colors() -> tuple:
    """Ask for fill color, background color, and transparency preference."""
    print("\n🎨 Color Options (press Enter for defaults, or type a name like 'blue'")
    print("   or a hex code like '#3498db'):")
    fill_color = resolve_color(prompt("Fill color (default black): "), "#000000")

    transparent = prompt("Transparent background? (y/N): ").lower() == "y"
    back_color = "transparent" if transparent else resolve_color(
        prompt("Background color (default white): "), "#ffffff"
    )
    return fill_color, back_color, transparent


def add_logo_if_requested(qr_image: Image.Image) -> Image.Image:
    """Optionally paste a logo image in the center of the QR code."""
    wants_logo = prompt("\nAdd a logo to the center? (y/N): ").lower() == "y"
    if not wants_logo:
        return qr_image

    logo_path = prompt("Path to logo image file: ")
    if not logo_path or not os.path.isfile(logo_path):
        print("⚠️  Logo file not found, skipping logo.")
        return qr_image

    try:
        qr_image = qr_image.convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")

        # Logo should take up roughly 1/4 of the QR code's width.
        qr_width, qr_height = qr_image.size
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size))

        position = (
            (qr_width - logo_size) // 2,
            (qr_height - logo_size) // 2,
        )
        qr_image.paste(logo, position, mask=logo)
        print("✅ Logo added.")
    except Exception as error:
        print(f"⚠️  Couldn't add logo ({error}), continuing without it.")

    return qr_image


# --------------------------------------------------------------------------- #
# Core QR generation
# --------------------------------------------------------------------------- #

def generate_qr_image(
    data: str,
    box_size: int,
    border: int,
    error_correction: int,
    fill_color: str,
    back_color: str,
    file_format: str,
):
    """
    Build the QR code object and return either a PIL Image (for png/jpg)
    or an SVG image object (for svg), ready to be saved.
    """
    if file_format == "svg":
        factory = qrcode.image.svg.SvgPathImage
        qr = qrcode.QRCode(
            error_correction=error_correction,
            box_size=box_size,
            border=border,
            image_factory=factory,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color=fill_color)

    qr = qrcode.QRCode(
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color=fill_color, back_color=back_color)


def save_qr_image(qr_image, filepath: str, file_format: str) -> None:
    """Save the QR image to disk, converting mode as needed per format."""
    if file_format == "svg":
        qr_image.save(filepath)
        return

    if file_format in ("jpg", "jpeg"):
        # JPG doesn't support transparency/alpha, so flatten onto white.
        rgb_image = qr_image.convert("RGB")
        rgb_image.save(filepath, quality=95)
    else:
        qr_image.save(filepath)


def preview_image(filepath: str, file_format: str) -> None:
    """Open the generated image in the system's default viewer, if possible."""
    if file_format == "svg":
        print("ℹ️  Preview isn't supported for SVG files — open it in a browser instead.")
        return
    try:
        Image.open(filepath).show()
    except Exception as error:
        print(f"⚠️  Couldn't open preview automatically ({error}).")


# --------------------------------------------------------------------------- #
# Main interactive flow for a single QR code
# --------------------------------------------------------------------------- #

def run_single_generation() -> None:
    """Handle the full flow: collect data, customize, generate, save."""
    data = collect_qr_data()

    box_size = choose_int("QR Size (box size)", default=10, minimum=1, maximum=50)
    border = choose_int("Border Size (min 4 recommended by spec)", default=4, minimum=0, maximum=20)
    error_correction = choose_error_correction()
    file_format = choose_file_format()
    fill_color, back_color, transparent = choose_colors()

    raw_filename = prompt("\nEnter filename (without extension, press Enter for default): ")
    filename = resolve_filename(raw_filename, file_format)

    qr_image = generate_qr_image(
        data=data,
        box_size=box_size,
        border=border,
        error_correction=error_correction,
        fill_color=fill_color,
        back_color=back_color,
        file_format=file_format,
    )

    if file_format != "svg":
        qr_image = add_logo_if_requested(qr_image)

    output_dir = ensure_output_dir()
    filepath = os.path.join(output_dir, filename)

    try:
        save_qr_image(qr_image, filepath, file_format)
    except PermissionError:
        print(f"❌ Permission denied while saving to '{filepath}'. Try a different filename or location.")
        return

    print("\n✅ QR Code Generated Successfully!")
    print("\nSaved At:\n")
    print(f"{filepath}")

    if prompt("\nShow preview now? (y/N): ").lower() == "y":
        preview_image(filepath, file_format)


def run_bulk_generation() -> None:
    """Generate one QR code per non-empty line in a user-supplied text file."""
    file_path = prompt("\nPath to the .txt file (one item per line): ")
    if not file_path or not os.path.isfile(file_path):
        print("❌ File not found. Please check the path and try again.")
        return

    with open(file_path, "r", encoding="utf-8") as handle:
        lines = [line.strip() for line in handle if line.strip()]

    if not lines:
        print("❌ The file is empty — nothing to generate.")
        return

    print(f"Found {len(lines)} item(s). Using default size/border/error-correction for all.")
    file_format = choose_file_format()
    output_dir = ensure_output_dir()

    successes = 0
    for index, line in enumerate(lines, start=1):
        try:
            qr_image = generate_qr_image(
                data=line,
                box_size=10,
                border=4,
                error_correction=ERROR_CORRECT_M,
                fill_color="#000000",
                back_color="#ffffff",
                file_format=file_format,
            )
            filename = f"qr_{index}.{file_format}"
            filepath = os.path.join(output_dir, filename)
            save_qr_image(qr_image, filepath, file_format)
            print(f"  ✅ [{index}/{len(lines)}] Saved: {filepath}")
            successes += 1
        except Exception as error:
            print(f"  ⚠️  [{index}/{len(lines)}] Skipped '{line}' due to error: {error}")

    print(f"\nDone! {successes}/{len(lines)} QR codes generated in '{output_dir}/'.")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def main() -> None:
    """Run the interactive menu loop until the user exits."""
    print_banner()

    while True:
        print_menu()
        try:
            choice = prompt("\nChoose an option: ")
        except EOFError:
            print("\n\n👋 Input stream closed. Goodbye!")
            sys.exit(0)

        try:
            if choice == "1":
                run_single_generation()
            elif choice == "2":
                run_bulk_generation()
            elif choice == "3":
                print("\n👋 Goodbye!")
                sys.exit(0)
            else:
                print("⚠️  Invalid option, please choose 1, 2, or 3.")
        except ValueError as error:
            print(f"❌ {error}")
        except EOFError:
            print("\n\n👋 Input stream closed. Goodbye!")
            sys.exit(0)
        except Exception as error:
            print(f"❌ Unexpected error: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Have a nice day!")
        sys.exit(0)