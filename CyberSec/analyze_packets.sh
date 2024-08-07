#!/bin/bash

# Path to the captured packets file
CAPTURE_FILE="/home/rex/Desktop/cyberSec/captured_packets.pcap"

# Path to the log file
LOG_FILE="/home/rex/Desktop/cyberSec/packet_analysis.log"

# Run tshark to analyze packets and save results
tshark -r "$CAPTURE_FILE" -q -z io,stat,1 > "$LOG_FILE"

# Display analysis result
cat "$LOG_FILE"

