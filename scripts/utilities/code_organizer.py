# code_organizer.py
import os
import hashlib

def organize_code_blocks(extracted_data, base_path="/storage/emulated/0/Documents/auto_build"):
    vibe_path = f"{base_path}/vibe"
    code_path = f"{base_path}/code"
    
    os.makedirs(vibe_path, exist_ok=True)
    os.makedirs(code_path, exist_ok=True)
    
    # Save vibe/flow
    vibe_file = f"{vibe_path}/conversation_{hashlib.md5(extracted_data['vibe_text'].encode()).hexdigest()[:8]}.txt"
    with open(vibe_file, 'w') as f:
        f.write(extracted_data['vibe_text'])
    
    # Organize code by type
    for lang, blocks in extracted_data['code_blocks'].items():
        if blocks:
            lang_dir = f"{code_path}/{lang}"
            os.makedirs(lang_dir, exist_ok=True)
            
            for i, block in enumerate(blocks):
                filename = f"{lang_dir}/block_{i+1}.{lang if lang != 'bash' else 'sh'}"
                with open(filename, 'w') as f:
                    f.write(block)
    
    return {
        'vibe_file': vibe_file,
        'code_path': code_path,
        'total_blocks': sum(len(blocks) for blocks in extracted_data['code_blocks'].values())
    }