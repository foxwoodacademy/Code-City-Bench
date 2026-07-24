def scan_and_register(directory):
    import os, json
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                print(f'[SKILL_FOUND] {os.path.join(root, file)}')
