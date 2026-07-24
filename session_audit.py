import sqlite3

DB_PATH = "/storage/emulated/0/RootBase/lough_telemetry.db"

def analyze_active_session():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Pull total data metrics collected in the ledger
        cursor.execute("SELECT COUNT(*) FROM telemetry_logs")
        total_packets = cursor.fetchone()[0]
        
        if total_packets == 0:
            print("\n[*] The telemetry database ledger is currently empty. Run the daemon to collect live data.")
            return

        # Count occurrences of safety anomalies flagged by the FEP loop
        cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE fep_status = 'CRITICAL_LOW_STRETCH_TEAR_RISK'")
        tear_warnings = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM telemetry_logs WHERE fep_status = 'CLIENT_PAIN_BREAKTHROUGH'")
        pain_spikes = cursor.fetchone()[0]
        
        # Calculate safety metrics mathematically
        tear_percentage = (tear_warnings / total_packets) * 100
        pain_percentage = (pain_spikes / total_packets) * 100
        
        print("\n" + "="*60)
        print(" LOUGH LIVE SESSION BIO-METRIC INTEGRITY REPORT")
        print("="*60)
        print(f" Total Tracked Frames Logged : {total_packets}")
        print(f" Dermis Tear Risk Incidents  : {tear_warnings} ({tear_percentage:.1f}%)")
        print(f" Client Pain Breakthroughs   : {pain_spikes} ({pain_percentage:.1f}%)")
        print("-"*60)
        
        if tear_percentage > 5.0:
            print(" [!] FIELD NOTICE: High tear risk ratio detected. Ensure the left hand")
            print("     maintains constant mechanical surface tension across the workspace.")
        else:
            print(" [->] FIELD STATUS: Structural dermis protection bounds maintained.")
            
        print("="*60 + "\n")
        conn.close()
        
    except sqlite3.OperationalError:
        print(f"\n[!] Error: Telemetry ledger file not found at {DB_PATH}")

if __name__ == "__main__":
    analyze_active_session()
