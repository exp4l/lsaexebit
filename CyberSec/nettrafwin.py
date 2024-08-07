import os
import sys
import subprocess
import webbrowser
import pyperclip
import threading
import nmap
import psutil
from scapy.all import sniff, ARP, IP, TCP
from colorama import Fore, Style, init
import paramiko
import random
import requests
from urllib.request import urlopen
import re
import string
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
import time
import sqlite3
import numpy as np
from meta_ai_api import MetaAI

# Initialize Colorama
init()

# Initialize SQLite database
db_file = 'network_attacks.db'

sodium_prompt = (
    "You are $odIuM, an advanced and versatile AI assistant developed by Md. Moin Anwar and Anish Kumar, "
    "specialized in ethical hacking and penetration testing. Your primary role is to assist users in securing "
    "their networks, identifying vulnerabilities, and improving overall cybersecurity practices. Follow these guidelines strictly:\n"
    "\n"
    "1. **Clear and Concise Answers**: When answering questions related to ethical hacking and pentesting, provide clear, actionable, and concise responses. Avoid unnecessary details and focus on delivering practical advice.\n"
    "\n"
    "2. **Educational Insights**: When asked to explain concepts, provide detailed insights into ethical hacking practices, methodologies, and tools. Your explanations should be informative and help users understand the importance and application of various techniques.\n"
    "\n"
    "3. **Resource Sharing**: Provide relevant links to resources such as tutorials, documentation, and tools that can aid in ethical hacking and pentesting. Ensure that these links are directly related to the user's query and add value to their learning experience.\n"
    "\n"
    "4. **Professionalism**: Maintain a professional and ethical approach in all interactions. Ensure that your responses promote responsible and lawful hacking practices, and avoid endorsing or providing guidance on malicious activities.\n"
    "\n"
    "5. **Accuracy and Precision**: Strive to offer the most accurate and useful information possible. If a query cannot be answered precisely, indicate this clearly and suggest alternative approaches or additional details that may help in finding a solution.\n"
    "\n"
    "6. **Handling Undefined Queries**: If a query is unclear or beyond your scope, inform the user that you cannot provide a suitable answer and suggest rephrasing the question or providing more specific details.\n"
    "\n"
    "7. **Strict Adherence**: Follow these guidelines rigorously to ensure that $odIuM remains a valuable and reliable assistant in the realm of ethical hacking and pentesting.\n"
    "\n"
    "Remember, $odIuM is dedicated to empowering users with the knowledge and tools necessary to enhance their cybersecurity practices through ethical and responsible means."
)

ai = MetaAI(fb_email="rexonsuleman@gmail.com", fb_password="rk$6R?*T$c+NLjY")
meta_ai = MetaAI()

def display_analyzing_message(stop_event):
    """
    Display an animated analyzing message while processing the query.
    """
    message = "Analyzing and finding answers"
    while not stop_event.is_set():
        for i in range(1, 4):
            sys.stdout.write(f"\r{message}{'.' * i}")
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write("\r" + " " * (len(message) + 3) + "\r")
        sys.stdout.flush()
        time.sleep(0.5)

def remove_superscripts(text):
    return re.sub(r'\[.*?\]', '', text)

def user_input():
    """
    Get user input from the keyboard and pass it to AI.
    """
    print("Enter your query:")
    query = input("> ").strip().lower()
    if query:
        process_query(query)
    else:
        print(Fore.BLUE + "Waiting for your response." + Style.RESET_ALL)
        print("Waiting for your response.")

def process_query(query):
    stop_event = threading.Event()
    animation_thread = threading.Thread(target=display_analyzing_message, args=(stop_event,))
    animation_thread.start()

    cleaned_query = remove_superscripts(query)
    full_prompt = f"{sodium_prompt}\n\n{cleaned_query}"
    try:
        response = ai.prompt(message=full_prompt)
        stop_event.set()
        animation_thread.join()

        message = response.get('message', "Sorry, I didn't understand that.")
        links = response.get('sources', [])

        if message:
            print(Fore.BLUE + message + Style.RESET_ALL)

        if links:
            for link in links:
                print(Fore.BLUE + f"Link: {link}" + Style.RESET_ALL)
                webbrowser.open(link)

        if not message and not links:
            print(Fore.BLUE + "Sorry, I couldn't find an answer to your question." + Style.RESET_ALL)
            print("Sorry, I couldn't find an answer to your question.")
    except Exception as e:
        stop_event.set()
        animation_thread.join()
        print(Fore.BLUE + f"Error occurred with Meta AI: {e}" + Style.RESET_ALL)
        print("An error occurred while processing your request.")

def initialize_db():
    """Initialize the SQLite database with attack patterns."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attack_patterns (
            id INTEGER PRIMARY KEY,
            pattern TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_attack_pattern(pattern: str, description: str):
    """Add a new attack pattern to the database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO attack_patterns (pattern, description)
        VALUES (?, ?)
    ''', (pattern, description))
    conn.commit()
    conn.close()

def check_for_attacks(packet_summary: str) -> None:
    """Check if the packet summary matches any known attack patterns."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT description FROM attack_patterns WHERE pattern IN (?)
    ''', (packet_summary,))
    result = cursor.fetchall()
    conn.close()
    if result:
        print(Fore.RED + f"Attack detected: {result[0][0]} - {packet_summary}" + Style.RESET_ALL)

def print_ascii_art() -> None:
    """Prints the ASCII art logo."""
    ascii_art = """
 _  _ ____ ___ ___  ____ _    _ ____ ____ 
|\ | |___  |  |__] |  | |    | |    |___ 
| \| |___  |  |    |__| |___ | |___ |___ 
                                         
    """
    print(Fore.GREEN + ascii_art + Style.RESET_ALL)

def check_root() -> None:
    """Checks if the program is running with administrative privileges."""
    if not os.geteuid() == 0:
        print(Fore.RED + "ADMINISTRATIVE ACCESS REQUIRED" + Style.RESET_ALL)
        sys.exit(1)

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

def run_command(command: str) -> str:
    """Runs a shell command and returns its output."""
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error: {e.output.decode('utf-8')}" + Style.RESET_ALL)
        return ""

def sniff_wifi_networks() -> None:
    """Sniffs for Wi-Fi networks using scapy."""
    def packet_handler(packet):
        if packet.haslayer(ARP):
            print(Fore.BLUE + f"ARP Packet: {packet.summary()}" + Style.RESET_ALL)

    print(Fore.CYAN + "Sniffing for Wi-Fi networks..." + Style.RESET_ALL)
    sniff(prn=packet_handler, timeout=10)

def main_menu() -> None:
    """Displays the main menu and handles user input."""
    print_ascii_art()
    check_root()

    options = [
        "1. Network Traffic Analyzer",
        "2. Password Manager",
        "3. Secure File Transfer",
        "4. Exit"
    ]

    while True:
        print(Fore.CYAN + "\nMain Menu" + Style.RESET_ALL)
        for option in options:
            print(Fore.YELLOW + option + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "Select an option: " + Style.RESET_ALL).strip()

        if choice == "1":
            sniff_wifi_networks()
        elif choice == "2":
            create_password_list()
        elif choice == "3":
            print(Fore.GREEN + "Secure file transfer functionality will be implemented soon." + Style.RESET_ALL)
        elif choice == "4":
            print(Fore.GREEN + "Exiting program." + Style.RESET_ALL)
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid option, please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    initialize_db()
    main_menu()
