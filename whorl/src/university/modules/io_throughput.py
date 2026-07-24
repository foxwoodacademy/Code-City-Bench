import time

class IOThroughputAnalyzer:
    """Real-world class for benchmarking I/O throughput."""
    
    @staticmethod
    def benchmark_write(data: bytes, path: str):
        """Writes data to disk and measures throughput."""
        start = time.time()
        with open(path, 'wb') as f:
            f.write(data)
        end = time.time()
        
        duration = end - start
        if duration == 0: duration = 0.000001
        return len(data) / duration # Bytes per second
