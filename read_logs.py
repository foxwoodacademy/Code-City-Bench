import sqlite3

DB_PATH = "/storage/emulated/0/RootBase/lough_telemetry.db"

def display_latest_logs(limit=10):
    """
    Connects to the local SQLite database and prints out the most recent entries.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Query the most recent logs recorded by the ingestion daemon
        cursor.execute('''
            SELECT id, timestamp, stretch_kpa, counter_emf_ma, fep_status 
            FROM telemetry_logs 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        
        print("\n" + "="*80)
        print(f" LOUGH SYSTEM TELEMETRY LEDGER - LATEST {limit} LOG ENTRIES")
        print("="*80)
        print(f"{'ID':<6} | {'Timestamp':<19} | {'Stretch (kPa)':<13} | {'Current (mA)':<12} | {'FEP Status'}")
        print("-"*80)
        
        for row in rows:
            print(f"{row[0]:<6} | {row[1]:<19} | {row[2]:<13.1f} | {row[3]:<12.1f} | {row[4]}")
            
        print("="*80 + "\n")
        conn.close()
        
    except sqlite3.OperationalError:
        print(f"\n[!] Error: Could not find database file at {DB_PATH}.")
        print("[!] Make sure your lough_daemon.py script has run and written data first.\n")

if __name__ == "__main__":
    display_latest_logs()
