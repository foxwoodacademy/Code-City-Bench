import os
import logging
from datetime import datetime

# --- CRITICAL CONFIGURATION: PROJECT ROOT ---
# This path points to your main project folder containing 'modmind-brains' and 'modmind-mask'.
# NOTE: The space in 'ModMind - EquiNex' is handled correctly.
BUNDLER_ROOT = '/storage/emulated/0/code_bundles'

# List of file extensions the FTC should capture and bundle
FILE_TYPES_TO_BUNDLE = ('.py', '.ts', '.tsx', '.js', '.json', '.env', '.md', '.css')

# Define the output file name and path (will be saved one level up for easy access)
OUTPUT_FILE = os.path.join(os.path.dirname(BUNDLER_ROOT), f"ModMind_Code_Bundle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Setup Logging to track the FTC's actions
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

def create_code_bundle():
    """Scans the project structure, concatenates all relevant code into one file."""
    
    # 1. Check if the project root exists
    if not os.path.isdir(BUNDLER_ROOT):
        logger.error(f"FATAL: BUNDLER_ROOT not found: {BUNDLER_ROOT}")
        logging.info("\nFATAL ERROR: Please check the folder path above.")
        return

    logging.info(f"\n--- FTC V1.0 Code Bundler Starting ---")
    logging.info(f"Scanning directory: {os.path.basename(BUNDLER_ROOT)}")
    
    bundled_files_count = 0
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        
        # os.walk iterates through the directory structure recursively
        for root, dirs, files in os.walk(BUNDLER_ROOT):
            
            # Skip the hidden .git directory and any local node_modules (if they exist)
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'dist']]
            
            for file_name in files:
                
                # Check if the file is a type we want to bundle
                if file_name.lower().endswith(FILE_TYPES_TO_BUNDLE):
                    file_path = os.path.join(root, file_name)
                    
                    # Create a relative path for the file header
                    relative_path = os.path.relpath(file_path, BUNDLER_ROOT)
                    
                    # Write a clear markdown header to separate the files
                    header = f"\n\n### FILE: {relative_path}\n"
                    outfile.write(header)
                    
                    # Use a triple backtick fence to contain the code block (Markdown format)
                    outfile.write("```\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            outfile.write(content)
                        
                        outfile.write("\n```\n")
                        logging.info(f"✅ Bundled: {relative_path}")
                        bundled_files_count += 1
                        
                    except UnicodeDecodeError:
                        error_msg = f"ERROR: Skipped {relative_path} (Decoding error, likely binary/unreadable)."
                        outfile.write(f"\n[FTC ERROR: {error_msg}]\n")
                        logging.info(f"❌ {error_msg}")
                    except Exception as e:
                        error_msg = f"ERROR: Skipped {relative_path} (General error: {e})."
                        outfile.write(f"\n[FTC ERROR: {error_msg}]\n")
                        logging.info(f"❌ {error_msg}")

    logging.info(f"\n--- FTC V1.0 Code Bundler Complete ---")
    logging.info(f"✅ Total Files Bundled: {bundled_files_count}")
    logging.info(f"OUTPUT FILE READY for one-click upload: {os.path.basename(OUTPUT_FILE)}")


if __name__ == "__main__":
    create_code_bundle()
