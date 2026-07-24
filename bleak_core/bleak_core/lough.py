import numpy as np

class LoughFieldOperator:
    """
    FEP Runtime Engine (Ultra-Optimized): Eliminates overhead for high-fidelity 
    telemetry by utilizing direct memory buffers.
    """
    def __init__(self, size=(100, 100)):
        self.size = size
        self.field = np.zeros(size, dtype=np.float32)

    def propagate(self, source_coord, intensity):
        """Ultra-fast propagation with minimal memory overhead."""
        x, y = source_coord
        self.field[x, y] += intensity
        
        # In-place Gaussian noise, avoiding intermediate buffer creation
        self.field += np.random.normal(0, 0.01, self.size)
        
        # In-place clip
        np.clip(self.field, 0, 1, out=self.field)
        return self.field

    def get_state(self):
        # Returning the buffer directly instead of converting to list
        return self.field
