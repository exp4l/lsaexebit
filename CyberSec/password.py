from colorama import Fore, Style, init
import string
import random
def create_password_list() -> None:
    """Creates a list of random passwords based on user criteria."""
    print(Fore.CYAN + "Password Creator" + Style.RESET_ALL)
    
    try:
        length = int(input(Fore.YELLOW + "Enter password length: " + Style.RESET_ALL).strip())
        use_uppercase = input(Fore.YELLOW + "Include uppercase letters? (y/n): " + Style.RESET_ALL).strip().lower() == 'y'
        use_numbers = input(Fore.YELLOW + "Include numbers? (y/n): " + Style.RESET_ALL).strip().lower() == 'y'
        use_special = input(Fore.YELLOW + "Include special characters? (y/n): " + Style.RESET_ALL).strip().lower() == 'y'
        count = int(input(Fore.YELLOW + "Enter number of passwords to generate: " + Style.RESET_ALL).strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter valid numbers." + Style.RESET_ALL)
        return

    def generate_password(length: int, use_uppercase: bool, use_numbers: bool, use_special: bool) -> str:
        """Generates a random password."""
        characters = string.ascii_lowercase
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        return ''.join(random.choice(characters) for _ in range(length))

    passwords = [generate_password(length, use_uppercase, use_numbers, use_special) for _ in range(count)]

    print(Fore.CYAN + "\nGenerated Passwords:" + Style.RESET_ALL)
    for i, pwd in enumerate(passwords, 1):
        print(Fore.GREEN + f"{i}: {pwd}" + Style.RESET_ALL)