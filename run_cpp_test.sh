#!/bin/bash

echo "[*] Step 1: Writing C++ Verification Source File..."

cat > /storage/emulated/0/RootBase/telemetry_test.cpp << 'C_CODE'
#include <iostream>
#include <cstdint>
#include <cstring>

// Exact 23-byte packed struct matching the hardware interface spec
struct __attribute__((__packed__)) TelemetryPacket {
    uint8_t  needle_id;          // 1 Byte
    float    left_hand_stretch;  // 4 Bytes
    float    counter_emf;        // 4 Bytes
    float    client_masseter;    // 4 Bytes
    float    artist_forearm;     // 4 Bytes
    uint16_t client_pulse;       // 2 Bytes
};

int main() {
    std::cout << "========================================\n";
    std::cout << " LOUGH STRUCT STRUCTURAL MEMORY AUDIT  \n";
    std::cout << "========================================\n";

    // 1. Verify byte alignments to prevent packet fragmentation
    std::cout << "[*] Expected Packet Size: 23 Bytes\n";
    std::cout << "[*] Compiled Struct Size: " << sizeof(TelemetryPacket) << " Bytes\n";

    if (sizeof(TelemetryPacket) == 23) {
        std::cout << " -> STATUS: SUCCESS. Memory boundaries align perfectly.\n";
    } else {
        std::cout << " -> ERROR: Memory misalignment detected!\n";
    }

    // 2. Initialize a mock packet data frame for logging verification
    TelemetryPacket mock_frame;
    mock_frame.needle_id = 0x02;            // 07RL Liner
    mock_frame.left_hand_stretch = 8.5f;    // Dangerously low tension (kPa)
    mock_frame.counter_emf = 145.2f;        // Heavy motor load resistance (mA)
    mock_frame.client_masseter = 45.0f;     // Relaxed jaw threshold (uV)
    mock_frame.artist_forearm = 110.5f;     // Steady focus activation (Hz)
    mock_frame.client_pulse = 72;           // Normal resting baseline (BPM)

    std::cout << "\n========================================\n";
    std::cout << " TELEMETRY DATA FRAME VALUE DUMP        \n";
    std::cout << "========================================\n";
    std::cout << " Needle Profile ID : 0x" << std::hex << (int)mock_frame.needle_id << "\n";
    std::cout << " Left Hand Stretch : " << std::dec << mock_frame.left_hand_stretch << " kPa\n";
    std::cout << " Counter-EMF Current: " << mock_frame.counter_emf << " mA\n";
    std::cout << " Client Masseter    : " << mock_frame.client_masseter << " uV\n";
    std::cout << " Artist Forearm     : " << mock_frame.artist_forearm << " Hz\n";
    std::cout << " Client Pulse Rate  : " << mock_frame.client_pulse << " BPM\n";
    std::cout << "========================================\n";

    return 0;
}
C_CODE

echo "[*] Step 2: Compiling C++ code with g++ (clang)..."
g++ -O2 /storage/emulated/0/RootBase/telemetry_test.cpp -o /storage/emulated/0/RootBase/telemetry_bin

echo "[*] Step 3: Executing local compiled binary..."
/storage/emulated/0/RootBase/telemetry_bin

