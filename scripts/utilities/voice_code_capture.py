import logging

#!/usr/bin/env python3
"""
VOICE CODE CAPTURE - Actually speaks and generates code
"""
import subprocess
import os
from chat_code_capture import ChatCodeCapture

class VoiceCodeCapture:
    def __init__(self):
        self.capture = ChatCodeCapture()
    
    def speak(self, text):
        """Actually speak using espeak"""
        try:
            # Clean text for espeak
            clean_text = text.replace('"', '').replace("'", "")
            subprocess.run(['espeak', '-s', '150', clean_text], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logging.info(f"🔊: {text}")
            return True
        except Exception as e:
            logging.info(f"🔇 TTS Failed: {e}")
            return False
    
    def process_with_voice(self, command):
        """Process command with voice feedback"""
        self.speak(f"Processing {command}")
        
        result = self.capture.capture_chat_command(command)
        
        if result and result["status"] == "SUCCESS":
            self.speak(f"Generated {len(result['files'])} files for {command}")
            return True
        else:
            self.speak("Generation failed")
            return False
    
    def live_voice_mode(self):
        """Live mode with actual voice"""
        self.speak("Voice code capture activated")
        
        logging.info("🎤 VOICE CAPTURE ACTIVE!")
        logging.info("I'll speak confirmations for every command")
        
        while True:
            try:
                command = input("💬 COMMAND: ").strip()
                
                if command.lower() in ['exit', 'quit']:
                    self.speak("Voice capture ended")
                    break
                
                self.process_with_voice(command)
                
            except KeyboardInterrupt:
                self.speak("Capture stopped")
                break

def main():
    voice_capture = VoiceCodeCapture()
    voice_capture.live_voice_mode()

if __name__ == "__main__":
    main()