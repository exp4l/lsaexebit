from colorama import Fore, Style, init

def run_command(command):
    """Executes a shell command."""
    import subprocess
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception(f"Command failed with error: {result.stderr.decode('utf-8')}")
    return result.stdout.decode('utf-8')

def install_tools():
    """Install necessary tools including Metasploit Framework, Nmap, and Scapy."""
    print(Fore.CYAN + "Installing necessary tools..." + Style.RESET_ALL)

    # Update package list
    print(Fore.YELLOW + "Updating package list..." + Style.RESET_ALL)
    run_command("apt-get update")
    # Install Metasploit Framework manually
    print(Fore.YELLOW + "Installing Metasploit Framework..." + Style.RESET_ALL)
    try:
        run_command("cd /tmp && curl -LO https://github.com/rapid7/metasploit-framework/archive/refs/heads/master.zip")
        run_command("unzip master.zip")
        run_command("cd metasploit-framework-master && sudo gem install bundler && bundle install")
        print(Fore.GREEN + "Metasploit Framework installed successfully." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Failed to install Metasploit Framework: {e}" + Style.RESET_ALL)

    # Install Nmap
    print(Fore.YELLOW + "Installing Nmap..." + Style.RESET_ALL)
    try:
        run_command("apt-get install -y nmap")
        print(Fore.GREEN + "Nmap installed successfully." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Failed to install Nmap: {e}" + Style.RESET_ALL)

    # Install Scapy
    print(Fore.YELLOW + "Installing Scapy..." + Style.RESET_ALL)
    try:
        run_command("pip install scapy")
        print(Fore.GREEN + "Scapy installed successfully." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Failed to install Scapy: {e}" + Style.RESET_ALL)