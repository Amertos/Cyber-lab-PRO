import base64
import binascii

def encode_b64(text):
    return base64.b64encode(text.encode()).decode()

def decode_b64(text):
    try: return base64.b64decode(text.encode()).decode()
    except: return "Error: Invalid Base64"

def encode_hex(text):
    return binascii.hexlify(text.encode()).decode()

def decode_hex(text):
    try: return binascii.unhexlify(text.encode()).decode()
    except: return "Error: Invalid Hex"
