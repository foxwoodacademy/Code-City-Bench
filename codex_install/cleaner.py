import os
import shutil

def clean_deep(base_dir):
    for root, dirs, files in os.walk(base_dir):
        # Clean node_modules, .git, __pycache__, and .tmp directories
        for d in dirs:
            if d in ["node_modules", "__pycache__", ".git", ".tmp", "dist", "build"]:
                path = os.path.join(root, d)
                print(f"[CLEAN] Removing: {path}")
                shutil.rmtree(path)
        
        # Clean stray zip/tar artifacts after extraction
        for f in files:
            if f.endswith(('.zip', '.tar', '.gz')):
                print(f"[CLEAN] Removing artifact: {f}")
                os.remove(os.path.join(root, f))

if __name__ == "__main__":
    clean_deep("/storage/emulated/0/RootBase")
