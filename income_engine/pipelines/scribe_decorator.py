import time
import functools
from pathlib import Path

# Grounding the logs inside your persistent storage path
LOG_DIR = Path("/storage/emulated/0/RootBase/income_engine/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
JOURNAL_FILE = LOG_DIR / "developer_journal.log"

def journal_entry(task_name):
    """
    A standard developer decorator to manually wrap critical functions.
    It records when a process starts, stops, and whether it succeeded.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(JOURNAL_FILE, "a") as f:
                f.write(f"[{timestamp}] START: {task_name} (Executing {func.__name__})\n")
            
            try:
                result = func(*args, **kwargs)
                
                completion_time = time.strftime("%Y-%m-%d %H:%M:%S")
                with open(JOURNAL_FILE, "a") as f:
                    f.write(f"[{completion_time}] SUCCESS: {task_name} completed cleanly.\n")
                return result
                
            except Exception as e:
                error_time = time.strftime("%Y-%m-%d %H:%M:%S")
                with open(JOURNAL_FILE, "a") as f:
                    f.write(f"[{error_time}] CRASH: {task_name} failed with error: {str(e)}\n")
                raise e
        return wrapper
    return decorator
