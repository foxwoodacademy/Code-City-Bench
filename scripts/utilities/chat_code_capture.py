import logging

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
        logging.info(f"🔊: {text}")
    except Exception as e:
        logging.info(f"🔇 TTS Error: {e}")

def extract_code_blocks(text):
    """Extract all code blocks from chat response"""
    # Match ```python ... ``` or ``` ... ```
    pattern = r'```(?:python)?\s*(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches if match.strip()]

def generate_filename(base_name, extension="py"):
    """Generate safe filenames that aren't too long"""
    # Clean the base name
    clean_name = re.sub(r'[^\w\s-]', '', base_name)
    clean_name = re.sub(r'[-\s]+', '_', clean_name)
    
    # Truncate if too long
    if len(clean_name) > 30:
        clean_name = clean_name[:30]
    
    # Add timestamp for uniqueness
    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"{clean_name}_{timestamp}.{extension}"
    
    return filename

def save_code_blocks(code_blocks, context=""):
    """Save extracted code blocks with smart naming"""
    saved_files = []
    
    for i, code in enumerate(code_blocks):
        if context:
            base_name = f"{context}_part{i+1}"
        else:
            base_name = f"generated_code_{i+1}"
            
        filename = generate_filename(base_name)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            saved_files.append(filename)
            logging.info(f"💾 SAVED: {filename}")
            speak(f"Saved {filename}")
            
        except Exception as e:
            logging.info(f"❌ Error saving {filename}: {e}")
    
    return saved_files

def main():
    speak("Chat code capture activated")
    logging.info("🎤 LIVE CHAT CAPTURE ACTIVATED!")
    logging.info("I'm now reading your chat commands and generating code...")
    logging.info("Paste chat responses with code blocks to extract and save")
    logging.info("Type 'exit' to quit\n")
    
    while True:
        try:
            logging.info("📝 PASTE CHAT RESPONSE: ", end="", flush=True)
            user_input = input().strip()
            
            if user_input.lower() == 'exit':
                speak("Exiting chat capture")
                break
                
            if user_input:
                logging.info("🎯 EXTRACTING CODE BLOCKS...")
                code_blocks = extract_code_blocks(user_input)
                
                if code_blocks:
                    saved_files = save_code_blocks(code_blocks, "extracted")
                    speak(f"Extracted {len(saved_files)} code files")
                    logging.info(f"✅ Saved {len(saved_files)} files")
                else:
                    logging.info("❌ No code blocks found")
                    speak("No code blocks found")
                    
        except KeyboardInterrupt:
            speak("Chat capture interrupted")
            logging.info("\n👋 Exiting...")
            break
        except Exception as e:
            logging.info(f"❌ Error: {e}")
            speak("Error processing command")

if __name__ == "__main__":
    main()
