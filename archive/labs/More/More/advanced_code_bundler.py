import logging

import os
import re
import zipfile
import time
from io import BytesIO

# --- CONFIGURATION ---
SUPPORTED_TEXT_EXTENSIONS = ['.txt', '.py', '.js', '.html', '.css', '.md']
SUPPORTED_ARCHIVE_EXTENSIONS = ['.zip']
# Mock extensions for features requiring external libraries
MOCK_EXTENSIONS = ['.rtf', '.pdf']
# ---------------------

def process_tags(content):
    """
    Scans content for specific task and project tags like #bsk and #task.
    Returns a list of identified tags and associated text.
    """
    tags_found = []
    # Regex to find tags followed by an optional colon and the rest of the line
    # (e.g., #bsk: This is the Blue Sky Task)
    tag_regex = r'(#(bsk|task|todo)[^\s:]*):?\s*(.*)'
    
    for match in re.finditer(tag_regex, content, re.IGNORECASE):
        full_tag = match.group(1).lower() # e.g., #bsk, #task-v3
        label = match.group(2).lower()    # e.g., bsk, task
        description = match.group(3).strip()
        
        tags_found.append({
            'tag': full_tag,
            'type': label,
            'description': description if description else f"No description found for {full_tag}"
        })
    return tags_found

def read_text_file(filepath):
    """Reads a standard text-based file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[ERROR: Could not read text file {filepath}: {e}]"

# --- MOCKED FUNCTIONS (Requires External Libraries in Pydroid3) ---

def mock_read_pdf(filepath):
    """
    MOCK FUNCTION: Reads text from a PDF file.
    
    To make this FUNCTIONAL in Pydroid3, you must install an external library:
    e.g., `pip install PyMuPDF` (highly recommended) or `pip install pdfminer.six`.
    Then, replace this function's body with the actual library logic.
    """
    logging.info(f"\n[ATTENTION: PDF PROCESSING MOCKED] To read '{filepath}' on Pydroid3, you need `pip install PyMuPDF`.")
    return f"[MOCK PDF CONTENT]: Successfully detected PDF at {filepath}. Replace this mock with PyMuPDF code."

def mock_read_rtf(filepath):
    """
    MOCK FUNCTION: Reads text from an RTF (Rich Text Format) file.

    To make this FUNCTIONAL in Pydroid3, you must install an external library:
    e.g., `pip install pyrtf-ng`.
    Then, replace this function's body with the actual library logic.
    """
    logging.info(f"\n[ATTENTION: RTF PROCESSING MOCKED] To read '{filepath}' on Pydroid3, you need `pip install pyrtf-ng`.")
    return f"[MOCK RTF CONTENT]: Successfully detected RTF at {filepath}. Replace this mock with pyrtf-ng code."

def mock_read_android_clipboard():
    """
    MOCK FUNCTION: Reads the content of the Android clipboard.

    To make this FUNCTIONAL in Pydroid3, this typically requires an Android-specific
    bridge or permissions, often necessitating a specific module available only
    to Pydroid3 (e.g., `android` module if available, or direct JNI calls).

    This implementation returns a placeholder.
    """
    logging.info("[ATTENTION: ANDROID CLIPBOARD MOCKED] Direct clipboard access requires specific Android API calls not available in standard Python. Check Pydroid3 documentation for their 'android' module if it exists.")
    return "[MOCK CLIPBOARD CONTENT]: Clipboard access not available in this environment."

# --- MAIN PROCESSORS ---

def process_file(filepath):
    """Handles individual file processing based on extension."""
    ext = os.path.splitext(filepath)[1].lower()
    content = ""
    
    if ext in SUPPORTED_TEXT_EXTENSIONS:
        content = read_text_file(filepath)
    elif ext == '.pdf':
        content = mock_read_pdf(filepath)
    elif ext == '.rtf':
        content = mock_read_rtf(filepath)
    else:
        # Ignore unsupported files, or add a log message
        return None

    if content:
        tags = process_tags(content)
        return {'filepath': filepath, 'content': content, 'tags': tags}
    return None

def process_zip(zip_path):
    """Processes contents within a ZIP file."""
    logging.info(f"\n--- Entering ZIP file: {zip_path} ---")
    results = []
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            for member in zip_file.namelist():
                if os.path.splitext(member)[1].lower() in SUPPORTED_TEXT_EXTENSIONS:
                    try:
                        # Extract file content directly to memory
                        with zip_file.open(member) as member_file:
                            content = member_file.read().decode('utf-8', errors='ignore')
                            tags = process_tags(content)
                            results.append({
                                'filepath': f"{zip_path}::{member}",
                                'content': content,
                                'tags': tags
                            })
                    except Exception as e:
                        logging.info(f"[ZIP ERROR]: Could not read {member} in zip: {e}")
        logging.info(f"--- Exiting ZIP file: {zip_path} ---")
        return results
    except Exception as e:
        logging.info(f"[ERROR]: Could not open ZIP file {zip_path}: {e}")
        return []

def code_bundler(root_path):
    """Main function to traverse directories and process files."""
    all_artifacts = []
    logging.info(f"Starting Code Bundler v3 Scan in: {root_path}")
    logging.info("-" * 40)
    
    # Check clipboard first (as per request)
    clipboard_content = mock_read_android_clipboard()
    clipboard_tags = process_tags(clipboard_content)
    all_artifacts.append({
        'filepath': '::ANDROID_CLIPBOARD::',
        'content': clipboard_content,
        'tags': clipboard_tags
    })
    
    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            ext = os.path.splitext(filename)[1].lower()
            
            if ext in SUPPORTED_ARCHIVE_EXTENSIONS:
                # Handle ZIP files
                zip_results = process_zip(full_path)
                all_artifacts.extend(zip_results)
            elif ext in SUPPORTED_TEXT_EXTENSIONS or ext in MOCK_EXTENSIONS:
                # Handle text, mock PDF, and mock RTF files
                file_result = process_file(full_path)
                if file_result:
                    all_artifacts.append(file_result)
                    
    logging.info("-" * 40)
    logging.info("Scan Complete. Summary of Artifacts:")
    return all_artifacts

def main():
    """Example usage and result reporting."""
    # Create mock files for demonstration purposes
    logging.info("Setting up mock environment...")
    
    # 1. Mock file structure
    if not os.path.exists("test_data"):
        os.makedirs("test_data/sub_project")
    
    with open("test_data/task_list.txt", "w") as f:
        f.write("#task-priority-1: Implement ModMind dashboard integration.\n")
        f.write("Standard file content. No tags here.\n")
        f.write("#BSK: Begin Blue Sky Meeting on EquiNex UI consistency.\n")
    
    with open("test_data/sub_project/core.py", "w") as f:
        f.write("# This is a python file\n")
        f.write("def calculate(): #task: Fix off-by-one bug.\n")

    # 2. Mock a ZIP file (contains a txt file)
    with zipfile.ZipFile('test_data/archive.zip', 'w') as zipf:
        zipf.writestr('internal_doc.txt', '#task: Review security protocols.\nArchive content.')

    # 3. Mock PDF and RTF files (will trigger MOCK warnings)
    with open("test_data/report.pdf", "w") as f: pass
    with open("test_data/notes.rtf", "w") as f: pass

    # Run the bundler (scanning the 'test_data' directory)
    results = code_bundler('./test_data')

    # Report results
    logging.info("\n" + "=" * 50)
    logging.info("FINAL BUNDLER REPORT")
    logging.info("=" * 50)
    
    all_tags = []
    for artifact in results:
        if artifact['tags']:
            logging.info(f"\n[FILE: {artifact['filepath']}]")
            for tag in artifact['tags']:
                logging.info(f"  > {tag['tag']} ({tag['type'].upper()}): {tag['description']}")
                all_tags.append(tag)

    logging.info("\n" + "=" * 50)
    logging.info(f"TOTAL TAGS FOUND: {len(all_tags)}")
    logging.info("=" * 50 + "\n")

    # Cleanup mock files (optional)
    try:
        os.remove("test_data/task_list.txt")
        os.remove("test_data/sub_project/core.py")
        os.remove("test_data/archive.zip")
        os.remove("test_data/report.pdf")
        os.remove("test_data/notes.rtf")
        os.rmdir("test_data/sub_project")
        os.rmdir("test_data")
    except Exception:
        pass # Ignore errors during cleanup

if __name__ == '__main__':
    main()