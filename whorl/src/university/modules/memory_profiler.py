import os
import psutil

class MemoryProfiler:
    """Real-world class for profiling memory consumption of a process."""
    
    @staticmethod
    def get_memory_usage():
        """Returns current process memory usage in bytes."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss
