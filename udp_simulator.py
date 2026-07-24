import socket
import struct
import time
import random

UDP_IP = "127.0.0.1" # Target local loopback address
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("==================================================")
echo_msg = "[*] LOUGH Hardware Network Simulator Active..."
print(echo_msg)
print("[*] Broadcasting 19-byte telemetry packets over UDP port 5555...")
print("==================================================")

try:
    while True:
        # Simulate variable physical states
        # 10% chance to simulate a critical low-stretch skin tearing hazard
        if random.random() < 0.10:
            stretch = random.uniform(5.0, 9.5)      # Low tension risk state
            client_jaw = random.uniform(20.0, 50.0)  # Calm baseline
        # 10% chance to simulate a client pain breakthrough event
        elif random.random() < 0.20:
            stretch = random.uniform(14.0, 20.0)     # Good skin stretch
            client_jaw = random.uniform(130.0, 210.0)# Spike in jaw clench
        else:
            stretch = random.uniform(12.0, 22.0)     # Normal, stable stretch
            client_jaw = random.uniform(30.0, 60.0)  # Calm baseline

        needle_id = 0x02       # Hardcoded to 07RL profile
        counter_emf = random.uniform(100.0, 180.0) # Active engine load (mA)
        artist_forearm = random.uniform(90.0, 140.0) # Focused muscle wave (Hz)
        pulse = random.randint(68, 85)             # Client Heart Rate (BPM)

        # Pack data into strict, validated 19-byte binary structure (<BffffH)
        packet = struct.pack('<BffffH', needle_id, stretch, counter_emf, client_jaw, artist_forearm, pulse)
        
        # Broadcast packet over local socket
        sock.sendto(packet, (UDP_IP, UDP_PORT))
        
        time.sleep(0.5) # Broadcast every half-second for visibility testing

except KeyboardInterrupt:
    print("\n[*] Hardware network simulation ended cleanly.")
