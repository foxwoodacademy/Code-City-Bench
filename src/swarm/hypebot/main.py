from profiler import AttributeProfiler
from pitch_engine import PitchEngine

def main():
    profiler = AttributeProfiler()
    pitcher = PitchEngine()
    
    print("[+] Hype Manbot MVP: Profiling...")
    profile = profiler.profile()
    
    print("[+] Generating Pitch...")
    pitch = pitcher.generate_pitch(profile)
    
    print("\n--- HYPE PITCH ---")
    print(pitch)
    print("------------------")

if __name__ == "__main__":
    main()
