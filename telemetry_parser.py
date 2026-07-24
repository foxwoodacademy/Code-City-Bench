import json
import struct
import time

class SkinAsUITelemetry:
    """
    Parses and structures multi-channel bio-kinetic telemetry.
    Optimized for FEP (Field-Excited Programming) agent ingestion.
    """
    def __init__(self):
        # Master lookup for needle geometry constants
        self.NEEDLE_PROFILES = {
            0x01: {"name": "03RL", "points": 3,  "type": "liner",  "target_depth_mm": 1.5, "max_safe_force_n": 1.2},
            0x02: {"name": "07RL", "points": 7,  "type": "liner",  "target_depth_mm": 1.8, "max_safe_force_n": 1.8},
            0x03: {"name": "11RS", "points": 11, "type": "shader", "target_depth_mm": 1.2, "max_safe_force_n": 2.2},
            0x04: {"name": "15M1", "points": 15, "type": "magnum", "target_depth_mm": 1.0, "max_safe_force_n": 3.0}
        }
        
    def unpack_raw_packet(self, raw_bytes):
        """
        Unpacks dense 24-byte binary packets from ESP32/hardware layer over UDP.
        Struct layout: B (Needle ID), f (Stretch), f (EMF), f (Client Jaw), f (Artist Forearm), H (Pulse)
        """
        if len(raw_bytes) != 23:
            raise ValueError(f"Invalid packet size: {len(raw_bytes)} bytes. Expected 23.")
            
        unpacked = struct.unpack('<BffffH', raw_bytes)
        
        needle_id = unpacked[0]
        needle_meta = self.NEEDLE_PROFILES.get(needle_id, {"name": "UNKNOWN", "points": 1, "type": "generic", "target_depth_mm": 1.0, "max_safe_force_n": 1.0})
        
        return {
            "timestamp_epoch": time.time(),
            "hardware_metrics": {
                "needle_profile": needle_meta["name"],
                "needle_type": needle_meta["type"],
                "left_hand_stretch_kpa": round(unpacked[1], 2),
                "counter_emf_ma": round(unpacked[2], 2),
                "client_masseter_rms_uv": round(unpacked[3], 2),
                "artist_forearm_muap_hz": round(unpacked[4], 2),
                "client_pulse_bpm": unpacked[5]
            }
        }

    def evaluate_fep_state(self, parsed_frame):
        """
        Calculates field excitation adjustments based on biometric feedback.
        """
        metrics = parsed_frame["hardware_metrics"]
        stretch = metrics["left_hand_stretch_kpa"]
        emf = metrics["counter_emf_ma"]
        client_jaw = metrics["client_masseter_rms_uv"]
        
        # Default stable states
        voltage_modifier = 0.0
        field_anomaly = False
        alert_flag = "STABLE"
        
        # Rule 1: Dermis Tearing Prevention (Inadequate Left Hand Stretch)
        if stretch < 10.0 and emf > 50.0:
            voltage_modifier = -1.5  # Drop voltage sharply to stop cutting
            alert_flag = "CRITICAL_LOW_STRETCH_TEAR_RISK"
            field_anomaly = True
            
        # Rule 2: Client Pain Breakthrough Spike Detection
        elif client_jaw > 120.0:
            voltage_modifier = -0.8  # Soften hit
            alert_flag = "CLIENT_PAIN_BREAKTHROUGH"
            field_anomaly = True
            
        # Rule 3: Optimal Performance State
        elif 12.0 <= stretch <= 22.0 and emf > 100.0:
            alert_flag = "OPTIMAL_ENGAGEMENT"

        parsed_frame["fep_agent_state"] = {
            "voltage_target_delta_v": voltage_modifier,
            "anomaly_detected": field_anomaly,
            "system_status_flag": alert_flag
        }
        return parsed_frame

# --- QUICK VERIFICATION TEST LOOP ---
if __name__ == "__main__":
    parser = SkinAsUITelemetry()
    
    # Mocking binary incoming hardware stream:
    # Needle ID: 2 (07RL)
    # Left Stretch: 8.5 kPa (Dangerously low)
    # Counter EMF: 145.2 mA (Deep engagement)
    # Client Jaw sEMG: 45.0 uV (Baseline calm)
    # Artist Forearm MUAP: 110.5 Hz (Focused)
    # Client Pulse: 72 BPM
    mock_binary_packet = struct.pack('<BffffH', 2, 8.5, 145.2, 45.0, 110.5, 72)
    
    # Process pipeline
    telemetry_frame = parser.unpack_raw_packet(mock_binary_packet)
    fep_analyzed_frame = parser.evaluate_fep_state(telemetry_frame)
    
    # Clean JSON format printed out for logging inspection
    print(json.dumps(fep_analyzed_frame, indent=2))
