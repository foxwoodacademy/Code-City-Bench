import logging

# cj_encoder.py - Transforms human text into filter-proof gibberish

def cj_encode(text):
    """
    1. Replaces spaces with a period (.).
    2. Performs a ROT-1 on all alphabetic characters (a->b, z->a).
    """
    encoded_text = []
    
    for char in text:
        # Handle alphabetical characters (ROT-1)
        if 'a' <= char <= 'z':
            encoded_char = chr((ord(char) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            encoded_char = chr((ord(char) - ord('A') + 1) % 26 + ord('A'))
        
        # Replace spaces/newlines with a delimiter
        elif char.isspace():
            encoded_char = '.'
            
        # Keep other characters (punctuation, numbers) as is
        else:
            encoded_char = char
            
        encoded_text.append(encoded_char)
        
    return "".join(encoded_text)

def cj_decode(text):
    """
    Reverses the CJ-Encoder: ROT-25 (same as ROT-1 backward) and replaces '.' with ' '.
    """
    decoded_text = []
    
    for char in text:
        # Handle alphabetical characters (ROT-25 / -1)
        if 'a' <= char <= 'z':
            decoded_char = chr((ord(char) - ord('a') - 1 + 26) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            decoded_char = chr((ord(char) - ord('A') - 1 + 26) % 26 + ord('A'))
        
        # Replace delimiter with space
        elif char == '.':
            decoded_char = ' '
            
        # Keep other characters
        else:
            decoded_char = char
            
        decoded_text.append(decoded_char)
        
    return "".join(decoded_text).strip()

# --- Example Usage ---
original_text = "Blue Sky Meetings is my answer to Vibe Coding."
encoded_output = cj_encode(original_text)

logging.info(f"Original: {original_text}")
logging.info(f"Encoded:  {encoded_output}")
logging.info(f"Decoded:  {cj_decode(encoded_output)}")

# Example Encoded Output:
# Cmvf.Tlz.Nffujohs.jt.nz.botxfs.up.Wjcf.Dpejoh.
