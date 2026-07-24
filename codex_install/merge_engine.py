import os
import hashlib
import shutil
import difflib

def get_file_stats(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        return len(lines), hashlib.sha256("".join(lines).encode()).hexdigest(), lines

def merge_logic(src_path, dest_path):
    lines_s, hash_s, content_s = get_file_stats(src_path)
    lines_d, hash_d, content_d = get_file_stats(dest_path)

    if hash_s == hash_d:
        return # Exact duplicate

    print(f"[MERGE] Logic variance detected in {os.path.basename(dest_path)} (Src: {lines_s} lines, Dest: {lines_d} lines)")
    
    # Simple logic-merging strategy: Add unique imports and then append new functions
    with open(dest_path, 'a') as f:
        f.write("\n# --- Automerged Logic Start ---\n")
        f.writelines(content_s)
        f.write("\n# --- Automerged Logic End ---\n")

def process_drop(incoming_dir, repo_dir):
    for root, _, files in os.walk(incoming_dir):
        for f in files:
            if f.endswith('.py'):
                src = os.path.join(root, f)
                dest = os.path.join(repo_dir, f)
                
                if not os.path.exists(dest):
                    print(f"[NEW] {f} ingested.")
                    shutil.copy(src, dest)
                else:
                    merge_logic(src, dest)

if __name__ == "__main__":
    process_drop("/storage/emulated/0/RootBase/incoming", "/storage/emulated/0/RootBase/codex_skills_registry")
