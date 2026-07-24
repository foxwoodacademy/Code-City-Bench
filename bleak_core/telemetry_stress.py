import time
import numpy as np
from bleak_core.lough import LoughFieldOperator
from bleak_core.dataweaver import DataWeaver

def run_stress_test(samples=5000):
    field = LoughFieldOperator()
    weaver = DataWeaver()
    
    print(f"Starting FEP Telemetry Stress Test ({samples} samples)...")
    start = time.time()
    
    for i in range(samples):
        state = field.propagate((50, 50), 0.5)
        # Process raw array directly
        signal = weaver.weave(state, external_signal=1.0)
        
    end = time.time()
    print(f"Test complete. Total time: {end - start:.2f}s")
    print(f"Throughput: {samples/(end-start):.2f} ops/sec")

if __name__ == "__main__":
    run_stress_test()
