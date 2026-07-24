import socket
import struct
import sqlite3
import time

DB_PATH = "/storage/emulated/0/RootBase/lough_telemetry.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS telemetry_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        needle_id INTEGER,
        stretch_kpa REAL,
        counter_emf_ma REAL,
        client_jaw_uv REAL,
        artist_muap_hz REAL,
        pulse_bpm INTEGER,
        fep_status TEXT
    )
''')
conn.commit()

UDP_IP = "0.0.0.0"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("[*] LOUGH Daemon active. Listening on UDP port 5555 (19-Byte Packets)...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        # Enforce the strict 19-byte physical constraint
        if len(data) == 19:
            unpacked = struct.unpack('<BffffH', data)
            
            needle_id = unpacked[0]
            stretch = unpacked[1]
            counter_emf = unpacked[2]
            client_jaw = unpacked[3]
            artist_forearm = unpacked[4]
            pulse = unpacked[5]
            
            status_flag = "STABLE"
            if stretch < 10.0:
                status_flag = "CRITICAL_LOW_STRETCH_TEAR_RISK"
            elif client_jaw > 120.0:
                status_flag = "CLIENT_PAIN_BREAKTHROUGH"

            cursor.execute('''
                INSERT INTO telemetry_logs 
                (needle_id, stretch_kpa, counter_emf_ma, client_jaw_uv, artist_muap_hz, pulse_bpm, fep_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (needle_id, stretch, counter_emf, client_jaw, artist_forearm, pulse, status_flag))
            conn.commit()
            
            print(f"[PACKET 19B] Stretch: {stretch:.1f} kPa | Jaw: {client_jaw:.1f} uV | Status: {status_flag}")
except KeyboardInterrupt:
    print("\n[*] Shutting down LOUGH Daemon safely.")
    conn.close()
