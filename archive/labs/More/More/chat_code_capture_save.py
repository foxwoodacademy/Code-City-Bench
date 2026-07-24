#!/usr/bin/env python3
"""
CHAT CODE CAPTURE - Actually reads chat and generates code files
NO BULLSHIT VERSION - FIXED FILENAME ISSUES
"""
import sys
import os
import re
from datetime import datetime
import subprocess

def speak(text):
    """Automatically speak text using espeak"""
    try:
        # Clean the text for shell safety
        clean_text = text.replace('"', '\\"').replace('$', '\\$')
        # Speak at reasonable speed/pitch
        subprocess.run(['espeak', '-s', '150', '-p', '50', clean_text],
                      capture_output=True, timeout=10)
        print(f"#!/usr/bin/env python3
"""
CHAT CODE CAPTURE - Actually reads chat and generates code files
NO BULLSHIT VERSION - FIXED FILENAME ISSUES
"""
import sys
import os
import re
from datetime import datetime
from smart_coder import SmartCoder
import subprocess
import os

def speak(text):
    """Automatically speak text using espeak"""
    try:
        # Clean the text for shell safety
        clean_text = text.replace('"', '\\"').replace('$', '\\$')
        # Speak at reasonable speed/pitch
        subprocess.run(['espeak', '-s', '150', '-p', '50', clean_text], 
                      capture_output=True, timeout=10)
    except Exception as e:
        print(f"TTS Error: {e}")

# Example usage in your existing code:
# speak("Code generation complete")
# speak(f"Saved {filename}")

class ChatCodeCapture:
    def __init__(self):
        self.coder = SmartCoder()
        self.output_dir = "generated_code"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def capture_chat_command(self, command):
        """Actually capture and process chat commands"""
        print(f"🎯 CAPTURING: {command}")
        
        # Extract command type and description
        if command.startswith('#python'):
            return self.generate_python(command.replace('#python', '').strip())
        elif command.startswith('#react'):
            return self.generate_react(command.replace('#react', '').strip())
        elif command.startswith('#task'):
            return self.create_task(command.replace('#task', '').strip())
        else:
            print(f"❓ Unknown command: {command}")
            return None
    
    def generate_python(self, description):
        """Generate Python code and SAVE IT - FIXED FILENAME ISSUE"""
        print(f"🐍 GENERATING PYTHON: {description}")
        
        try:
            result = self.coder.generate_from_description(description, "python")
            
            # Actually save the files - WITH FIXED FILENAMES
            saved_files = []
            for original_filename, content in result["files"].items():
                # FIX: Create safe filename
                safe_filename = self.create_safe_filename(description, original_filename)
                filepath = os.path.join(self.output_dir, safe_filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files.append(filepath)
                print(f"💾 SAVED: {filepath}")
            
            return {
                "status": "SUCCESS", 
                "type": "python",
                "description": description,
                "files": saved_files,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"💥 GENERATION FAILED: {e}")
            return {"status": "ERROR", "error": str(e)}
    
    def generate_react(self, description):
        """Generate React code and SAVE IT - FIXED FILENAME ISSUE"""
        print(f"⚛️ GENERATING REACT: {description}")
        
        try:
            result = self.coder.generate_from_description(description, "react")
            
            # Actually save the files - WITH FIXED FILENAMES
            saved_files = []
            for original_filename, content in result["files"].items():
                # FIX: Create safe filename
                safe_filename = self.create_safe_filename(description, original_filename)
                filepath = os.path.join(self.output_dir, safe_filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                saved_files.append(filepath)
                print(f"💾 SAVED: {filepath}")
      
            except KeyboardInterrupt:
                print("\n🛑 Capture stopped.")
                break
            except Exception as e:
                print(f"💥 CAPTURE ERROR: {e}")

def main():
    capture = ChatCodeCapture()
    
    if len(sys.argv) > 1:
        # Process single command
        command = " ".join(sys.argv[1:])
        result = capture.capture_chat_command(command)
        if result:
            print(f"🎯 RESULT: {result['status']}")
    else:
        # Live capture mode
        capture.live_capture_mode()

if __name__ == "__main__":
    main()
