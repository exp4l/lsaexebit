#!/bin/bash

# Function to install Python
install_python() {
    echo "Installing Python..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # For Debian-based systems (e.g., Ubuntu)
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # For macOS
        brew install python
    else
        echo "Unsupported OS for automatic Python installation."
        return 1
    fi
}

# Function to install nmap
install_nmap() {
    echo "Installing nmap..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y nmap
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install nmap
    else
        echo "Unsupported OS for automatic nmap installation."
        return 1
    fi
}

# Function to install Metasploit
install_metasploit() {
    echo "Installing Metasploit..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl https://raw.githubusercontent.com/rapid7/metasploit-framework/master/msfupdate | sudo bash
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install metasploit
    else
        echo "Unsupported OS for automatic Metasploit installation."
        return 1
    fi
}

# Function to install Python packages from requirements.txt
install_python_packages() {
    echo "Installing Python packages..."
    pip3 install -r requirements.txt
}

# Function to handle installation on Windows
handle_windows_installation() {
    echo "You are on Windows. The script will attempt to use curl for downloads."

    # Install Python
    echo "Downloading Python installer..."
    curl -LO https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
    echo "Please run the downloaded installer and follow the instructions to install Python."

    # Install nmap
    echo "Downloading nmap installer..."
    curl -LO https://nmap.org/dist/nmap-7.93-setup.exe
    echo "Please run the downloaded installer and follow the instructions to install nmap."

    # Install Metasploit
    echo "Downloading Metasploit installer..."
    curl -LO https://downloads.metasploit.com/data/releases/metasploit-latest-windows-x64-installer.exe
    echo "Please run the downloaded installer and follow the instructions to install Metasploit."

    echo "After installing these, run the Python package installation manually."
}

# Check the operating system and perform installations
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    install_python
    install_nmap
    install_metasploit
    install_python_packages
elif [[ "$OSTYPE" == "cygwin"* || "$OSTYPE" == "msys"* ]]; then
    handle_windows_installation
else
    echo "Unsupported operating system."
    exit 1
fi

echo "Setup complete!"
