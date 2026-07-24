import os
import hashlib
import shutil

def get_file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def merge_scripts(src, dest):
    # Simple strategy: append if different
    with open(src, 'r') as s, open(dest, 'a') as d:
        d.write("\n# --- Merged from duplicate ---\n")
        d.write(s.read())

def dedup(incoming_dir, repo_dir):
    registry = {} # hash -> path
    for root, _, files in os.walk(repo_dir):
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                registry[get_file_hash(path)] = path

    for root, _, files in os.walk(incoming_dir):
        for f in files:
            if f.endswith('.py'):
                src = os.path.join(root, f)
                h = get_file_hash(src)
                if h in registry:
                    print(f"[SKIP] Duplicate: {f}")
                else:
                    dest = os.path.join(repo_dir, f)
                    if os.path.exists(dest):
                        print(f"[MERGE] {f} exists, merging logic...")
                        merge_scripts(src, dest)
                    else:
                        print(f"[NEW] {f} added.")
                        shutil.copy(src, dest)
                        registry[h] = dest

if __name__ == "__main__":
    dedup("/storage/emulated/0/RootBase/incoming", "/storage/emulated/0/RootBase/codex_skills_registry")
