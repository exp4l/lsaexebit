from colorama import Fore, Style, init
import subprocess

def run_command(command):
    """Executes a shell command and handles errors."""
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode('utf-8')
        if "Interface doesn't support scanning" in error_message:
            print(Fore.RED + "Interface doesn't support monitor mode." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Command failed with error: {error_message}" + Style.RESET_ALL)
        return ""

def sniff_wifi_networks() -> None:
    """Sniffs for nearby WiFi networks and estimates network congestion."""
    print(Fore.CYAN + "Sniffing WiFi Networks..." + Style.RESET_ALL)
    output = run_command("iwlist wlan0 scan")
    
    if not output:
        print(Fore.RED + "Failed to execute iwlist command." + Style.RESET_ALL)
        return

    print(Fore.GREEN + "Detected Networks:" + Style.RESET_ALL)
    network_count = 0
    freq = ""
    for line in output.split("\n"):
        if "Frequency:5.32 GHz" in line:
            freq = " (5G)"
        elif "Frequency:2.42 GHz" in line:
            freq = ""
        if "ESSID" in line:
            network_count += 1
            if "ESSID:\"\\x00\\x00\\x00\\x00\\x00\\x00\"" in line:
                print(Fore.RED + "Hidden Network" + freq + Style.RESET_ALL)
            else:
                essid = line.split("ESSID:")[1].strip().strip('"')
                print(Fore.GREEN + f"Network: {essid}" + freq + Style.RESET_ALL)
    print(Fore.GREEN + f"Total Networks: {network_count}" + Style.RESET_ALL)
    if network_count > 15:
        congestion_level = "High Network Congestion"
    elif 5 < network_count <= 15:
        congestion_level = "Mid-Level Network Congestion"
    else:
        congestion_level = "Low Network Congestion"
    print(Fore.GREEN + f"{congestion_level}." + Style.RESET_ALL)
