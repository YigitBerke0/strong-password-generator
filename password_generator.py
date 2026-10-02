import math
import random
import string
from datetime import datetime


def get_password_length() -> int:
    """Prompt user for password length with error handling."""
    while True:
        try:
            user_input = input("Enter desired password length (minimum 4): ").strip()
            length = int(user_input)
            if length < 4:
                print("  [!] Password length must be at least 4 characters. Please try again.")
                continue
            if length > 256:
                print("  [!] Password length cannot exceed 256 characters. Please try again.")
                continue
            return length
        except ValueError:
            print("  [!] Invalid input: Please enter a valid whole number.")


def get_difficulty_level() -> tuple[str, str, int]:
    """Prompt user to choose difficulty level with error handling.
    Returns (difficulty_name, character_pool, pool_size).
    """
    print("\nSelect Difficulty Level:")
    print("  1: Easy   [Letters only: a-z, A-Z]")
    print("  2: Medium [Letters + Digits: a-z, A-Z, 0-9]")
    print("  3: Hard   [Letters + Digits + Symbols: a-z, A-Z, 0-9, !@#$%...]")

    while True:
        try:
            choice = input("Enter difficulty (1, 2, or 3): ").strip()
            difficulty = int(choice)
            if difficulty == 1:
                pool = string.ascii_letters
                return "Easy (Letters only)", pool, len(pool)
            elif difficulty == 2:
                pool = string.ascii_letters + string.digits
                return "Medium (Letters + Digits)", pool, len(pool)
            elif difficulty == 3:
                pool = string.ascii_letters + string.digits + string.punctuation
                return "Hard (Letters + Digits + Symbols)", pool, len(pool)
            else:
                print("  [!] Invalid choice: Please enter 1, 2, or 3.")
        except ValueError:
            print("  [!] Invalid input: Please enter a number (1, 2, or 3).")


def generate_passwords(length: int, pool: str, count: int = 3) -> list[str]:
    """Generate distinct password options from the given pool."""
    options = set()
    max_attempts = 1000
    attempts = 0

    while len(options) < count and attempts < max_attempts:
        pwd = "".join(random.choice(pool) for _ in range(length))
        options.add(pwd)
        attempts += 1

    return list(options)


def select_password(passwords: list[str]) -> str:
    """Display generated passwords and prompt user to select one."""
    print("\nGenerated Password Options:")
    for idx, pwd in enumerate(passwords, start=1):
        print(f"  [{idx}] {pwd}")

    while True:
        try:
            selection = input(f"\nSelect a password to use (1-{len(passwords)}): ").strip()
            selected_idx = int(selection)
            if 1 <= selected_idx <= len(passwords):
                return passwords[selected_idx - 1]
            print(f"  [!] Please enter a number between 1 and {len(passwords)}.")
        except ValueError:
            print("  [!] Invalid input: Please enter a valid number.")


def get_password_label() -> str:
    """Prompt user for a custom name/label for the password."""
    while True:
        label = input("\nEnter a name/label for this password (e.g., 'Steam Account'): ").strip()
        if not label:
            print("  [!] Label cannot be empty. Please enter a valid name.")
            continue
        return label


def save_to_file(label: str, password: str, filename: str = "passwords.txt") -> bool:
    """Append the label and password to a local text file with error handling."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] Label: {label} | Password: {password}\n"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(entry)
        return True
    except OSError as err:
        print(f"\n[!] File Error: Could not save password to '{filename}': {err}")
        return False


def format_crack_time(seconds: float) -> str:
    """Format cracking time in seconds into human-readable duration."""
    if seconds < 1e-4:
        return "< 0.1 milliseconds (Instantly)"
    if seconds < 0.001:
        return f"{seconds * 1000:.2f} milliseconds (Instantly)"
    if seconds < 1:
        return f"{seconds:.3f} seconds (Almost instantly)"
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    if seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes ({seconds:,.0f} seconds)"
    if seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.2f} hours"
    if seconds < 31536000:  # 365 days
        days = seconds / 86400
        return f"{days:.2f} days"

    years = seconds / 31536000
    if years < 100:
        return f"{years:.2f} years"
    if years < 1_000:
        return f"{years:,.1f} years ({years / 100:.1f} centuries)"
    if years < 1_000_000:
        return f"{years:,.0f} years"
    if years < 1_000_000_000:
        million_years = years / 1_000_000
        return f"{million_years:,.2f} million years ({years:.2e} years)"
    if years < 1_000_000_000_000:
        billion_years = years / 1_000_000_000
        return f"{billion_years:,.2f} billion years ({years:.2e} years)"
    if years < 1_000_000_000_000_000:
        trillion_years = years / 1_000_000_000_000
        return f"{trillion_years:,.2f} trillion years ({years:.2e} years)"

    return f"{years:.2e} years (Astronomical / Infeasible)"


def display_security_info(
    label: str,
    password: str,
    difficulty_name: str,
    pool_size: int,
    file_saved: bool,
    filename: str = "passwords.txt",
):
    """Calculate brute-force cracking time and display a formatted info report."""
    length = len(password)
    total_combinations = pool_size**length
    entropy_bits = length * math.log2(pool_size)
    cracking_speed = 10_000_000_000
    crack_time_seconds = total_combinations / cracking_speed
    formatted_time = format_crack_time(crack_time_seconds)

    formatted_combinations = (
        f"{total_combinations:,}"
        if total_combinations < 10**15
        else f"{total_combinations:.3e}"
    )

    print("\n" + "=" * 65)
    print("                    [INFO] SECURITY REPORT")
    print("=" * 65)
    print(f"  Account / Label       : {label}")
    print(f"  Selected Password     : {password}")
    print(f"  Password Length       : {length} characters")
    print(f"  Difficulty Level      : {difficulty_name}")
    print(f"  Character Pool Size   : {pool_size} possible characters")
    print(f"  Information Entropy   : {entropy_bits:.2f} bits")
    print(f"  Total Combinations    : {formatted_combinations} (Formula: {pool_size}^{length})")
    print(f"  Assumed Attack Speed  : 10,000,000,000 guesses/sec (10 billion/s)")
    print(f"  Estimated Crack Time  : {formatted_time}")
    if file_saved:
        print(f"  Storage Status        : Appended successfully to '{filename}'")
    else:
        print(f"  Storage Status        : [!] Failed to append to '{filename}'")
    print("=" * 65 + "\n")


def main():
    print("=" * 65)
    print("          SECURE PASSWORD GENERATOR (CLI TOOL)")
    print("=" * 65)

    try:
        length = get_password_length()
        diff_name, pool, pool_size = get_difficulty_level()

        passwords = generate_passwords(length, pool, count=3)

        chosen_password = select_password(passwords)

        label = get_password_label()
        file_saved = save_to_file(label, chosen_password)

        display_security_info(
            label=label,
            password=chosen_password,
            difficulty_name=diff_name,
            pool_size=pool_size,
            file_saved=file_saved,
        )

        print("[+] Process completed successfully. Keep your passwords safe!\n")

    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user. Exiting...\n")


if __name__ == "__main__":
    main()
1