import os
import re

def purge_buzzwords():
    # Target replacements
    replacements = {
        r"ModMind\s+Entity": "ModMind Intelligence",
        r"ModMind\s+Stack": "ModMind Stack",
        r"ModMind\s+Bridge": "ModMind Bridge",
        r"ModMind\s+Guard": "MotherBrain Guard",
        r"ModMind\s+Vault": "MotherBrain Vault",
        r"ModMind\s+Valet": "JaneBot Valet",
        r"ModMind\s+Dashboard": "ModMind Dashboard",
        r"ModMind\s+Identity": "ModMind Identity",
        r"ModMind\s+Symmetry": "ModMind Symmetry",
        r"ModMind autonomy": "ModMind autonomy",
        r"ModMind": "ModMind"
    }

    root_dir = "/storage/emulated/0/RootBase/"
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(('.md', '.py', '.json', '.txt', '.html', '.js')):
                file_path = os.path.join(dirpath, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    for pattern, replacement in replacements.items():
                        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                    
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✅ Purged buzzwords from: {file_path}")
                except Exception as e:
                    print(f"❌ Failed to process {file_path}: {e}")

if __name__ == "__main__":
    purge_buzzwords()
