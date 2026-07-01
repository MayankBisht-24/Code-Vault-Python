import secrets
import string

YES = "Y"
NO = "N"
MAX_LENGTH = 24


def ask_yes_no(prompt):
    """
    Ask the user a yes/no question and keep asking until
    a valid Y or N is entered.
    """
    while True:
        answer = input(prompt).strip().upper()
        if answer in (YES, NO):
            return answer == YES
        print("Invalid input. Please enter Y or N.")


def get_user_preferences():
    """
    Collect password length and character type choices from the user.
    Keeps asking until the combination of inputs is valid.
    """
    while True:
        try:
            length = int(input("Password Length: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if length <= 0:
            print("Length must be greater than 0. Try again.")
            continue

        if length > MAX_LENGTH:
            print(f"Length must not exceed {MAX_LENGTH}. Try again.")
            continue

        use_upper = ask_yes_no("Include Uppercase? (Y/N): ")
        use_lower = ask_yes_no("Include Lowercase? (Y/N): ")
        use_digits = ask_yes_no("Include Numbers? (Y/N): ")
        use_symbols = ask_yes_no("Include Symbols? (Y/N): ")

        selected_types = sum([use_upper, use_lower, use_digits, use_symbols])

        if selected_types == 0:
            print("At least one character type must be selected.\n")
            continue

        if length < selected_types:
            print(f"Password length must be at least {selected_types} "
                  f"(the number of selected character types).\n")
            continue

        return length, use_upper, use_lower, use_digits, use_symbols


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """
    Generate a random password that respects the chosen length
    and guarantees at least one character from every selected type.
    Uses the secrets module since it's built for security-sensitive
    randomness, unlike the plain random module.
    """
    char_pool = ""
    required_chars = []

    # Build the character pool and reserve one guaranteed character per type
    if use_upper:
        char_pool += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        char_pool += string.ascii_lowercase
        required_chars.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        char_pool += string.digits
        required_chars.append(secrets.choice(string.digits))
    if use_symbols:
        char_pool += string.punctuation
        required_chars.append(secrets.choice(string.punctuation))

    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]

    # Shuffle so the guaranteed characters aren't always at the front
    shuffled = password_chars[:]
    for i in range(len(shuffled) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]

    return "".join(shuffled)


def check_password_strength(password, use_upper, use_lower, use_digits, use_symbols):
    """
    Give a rough strength rating based on length and character variety.
    Returns a label and a simple bar to display alongside it.
    """
    variety_score = sum([use_upper, use_lower, use_digits, use_symbols])
    length = len(password)

    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    score += variety_score

    if score <= 2:
        label, bar = "Weak", "██░░░░░░░░"
    elif score <= 4:
        label, bar = "Moderate", "█████░░░░░"
    elif score <= 6:
        label, bar = "Strong", "████████░░"
    else:
        label, bar = "Very Strong", "██████████"

    return label, bar


def main():
    print("=== Password Generator ===\n")

    while True:
        length, use_upper, use_lower, use_digits, use_symbols = get_user_preferences()
        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        label, bar = check_password_strength(password, use_upper, use_lower, use_digits, use_symbols)

        print(f"\nGenerated Password: {password}")
        print(f"Strength: {bar} {label}\n")

        if not ask_yes_no("Generate another password? (Y/N): "):
            print("Have a good day!")
            break
        print()


if __name__ == "__main__":
    main()