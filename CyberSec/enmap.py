from colorama import Fore, Style, init
import nmap
from idschecker import check_for_attacks
from scapy.all import sniff, ARP, IP, TCP
import paramiko
from sniffer import run_command

def start_ids() -> None:
    """Starts an Intrusion Detection System (IDS) to monitor network traffic."""
    def packet_callback(packet):
        if ARP in packet:
            print(Fore.BLUE + f"ARP Packet: {packet.summary()}" + Style.RESET_ALL)
        elif IP in packet:
            if TCP in packet:
                flags = packet[TCP].flags
                if flags == 0x10:  # ACK flag
                    packet_summary = f"Potential Nmap ACK Scan: {packet.summary()}"
                    print(Fore.RED + packet_summary + Style.RESET_ALL)
                    check_for_attacks(packet_summary)
                elif flags == 0x02:  # SYN flag
                    packet_summary = f"Potential Nmap SYN Scan: {packet.summary()}"
                    print(Fore.RED + packet_summary + Style.RESET_ALL)
                    check_for_attacks(packet_summary)
            print(Fore.YELLOW + f"IP Packet: {packet.summary()}" + Style.RESET_ALL)

    print(Fore.GREEN + "Starting IDS. Press Ctrl+C to stop." + Style.RESET_ALL)
    sniff(prn=packet_callback, store=0)

def port_scanner() -> None:
    """Scans ports on a target IP and displays results."""
    target_ip = input(Fore.YELLOW + "Enter target IP: " + Style.RESET_ALL).strip()
    
    while True:
        print(Fore.CYAN + "\nPort Scan Menu" + Style.RESET_ALL)
        print("1. SYN Scan (default) - Quick scan that checks if a port is open.")
        print("2. TCP Connect Scan - Comprehensive scan for all TCP ports.")
        print("3. UDP Scan - Checks for open UDP ports.")
        print("4. OS Detection - Attempts to detect the operating system of the target.")
        print("5. Service Version Detection - Detects service versions running on open ports.")
        print("0. Exit")
        
        choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()
        
        if choice == '0':
            break
        
        nm = nmap.PortScanner()
        command = ""
        
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
        
        print(Fore.CYAN + "Analyzing, please wait..." + Style.RESET_ALL)
        try:
            result = run_command(command)
            print(Fore.GREEN + "Scan Results:" + Style.RESET_ALL)
            print(result)
        except Exception as e:
            print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)
    """Scans ports on a target IP and displays results."""
    target_ip = input("Enter target IP: ")
    
    # Port scan menu
    print(Fore.YELLOW + "\nPort Scan Menu" + Style.RESET_ALL)
    print("1. SYN Scan (default) - Quick scan that checks if a port is open.")
    print("2. TCP Connect Scan - Comprehensive scan for all TCP ports.")
    print("3. UDP Scan - Checks for open UDP ports.")
    print("4. OS Detection - Attempts to detect the operating system of the target.")
    print("5. Service Version Detection - Detects service versions running on open ports.")
    print("0. Exit")
    
    choice = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL).strip()
    
    if choice == '0':
        return

    nm = nmap.PortScanner()
    scan_type = ""
    try:
        if choice == '1':
            scan_type = "SYN Scan"
            scan_results = nm.scan(target_ip, arguments='-sS')
        elif choice == '2':
            scan_type = "TCP Connect Scan"
            scan_results = nm.scan(target_ip, arguments='-sT')
        elif choice == '3':
            scan_type = "UDP Scan"
            scan_results = nm.scan(target_ip, arguments='-sU')
        elif choice == '4':
            scan_type = "OS Detection"
            scan_results = nm.scan(target_ip, arguments='-O')
        elif choice == '5':
            scan_type = "Service Version Detection"
            scan_results = nm.scan(target_ip, arguments='-sV')
        else:
            print(Fore.RED + "Invalid choice. Please select a valid scan option." + Style.RESET_ALL)
            return
        
        if not nm.all_hosts():
            print(Fore.RED + "No hosts found." + Style.RESET_ALL)
            return
        
        print(Fore.GREEN + "Scan Results:" + Style.RESET_ALL)
        for host in nm.all_hosts():
            print(f"\nHost: {host} ({nm[host].hostname()})")
            print(f"State: {nm[host].state()}")
            for proto in nm[host].all_protocols():
                print(f"\nProtocol: {proto}")
                lport = nm[host][proto].keys()
                for port in lport:
                    port_info = nm[host][proto][port]
                    print(f"Port: {port}")
                    print(f"    State: {port_info.get('state', '')}")
                    print(f"    Name: {port_info.get('name', '')}")
                    print(f"    Product: {port_info.get('product', '')}")
                    print(f"    Extra Info: {port_info.get('extrainfo', '')}")
                    print(f"    Reason: {port_info.get('reason', '')}")
                    print(f"    Version: {port_info.get('version', '')}")
                    print(f"    CPE: {port_info.get('cpe', '')}")

    except Exception as e:
        print(Fore.RED + f"Error occurred: {e}" + Style.RESET_ALL)