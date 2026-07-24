"""
CLI Entry point for NatCommand.
Usage: python3 nat.py 'save this vibe'
"""

import sys
import logging
from natcommand.core.parser import SemanticParser
from natcommand.core.actions import ActionHandler

logging.basicConfig(level=logging.INFO)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 nat.py '<command>'")
        return
        
    user_input = sys.argv[1]
    
    parser = SemanticParser()
    handler = ActionHandler()
    
    intent = parser.parse(user_input)
    handler.handle(intent)
    
    print(f"✅ Executed: {intent.action} | Input: '{user_input}'")

if __name__ == "__main__":
    main()
