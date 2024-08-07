import os
import random
import time

# Define the specific IP address of the phone
target_ip = "192.168.29.122"

# Define the range of ports or list of ports to randomize
port_range = list(range(1, 65536))  # Ports from 1 to 65535

def random_ports(port_range):
    """Randomly select a port from the list."""
    return random.choice(port_range)

def run_nmap_scan(target_ip, port):
    """Run nmap scan against the target IP and port."""
    command = f"nmap -p {port} {target_ip} -Pn"
    print(f"Running scan on {target_ip} for port {port}")
    os.system(command)

def main():
    while True:
        # Randomly select a port
        port = random_ports(port_range)
        
        # Run nmap scan
        run_nmap_scan(target_ip, port)
        
        # Wait before running the next scan (e.g., 60 seconds)
        time.sleep(60)

if __name__ == "__main__":
    main()
