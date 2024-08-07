from colorama import Fore, Style, init
import sqlite3
db_file = 'network_attacks.db'
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