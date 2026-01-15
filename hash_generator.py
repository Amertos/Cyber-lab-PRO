import hashlib
import argparse

# Try importing bcrypt, handle it gracefully if user hasn't pip installed it
try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

def get_hashes(text):
    """
    Returns a dictionary of hash data.
    """
    encoded_text = text.encode('utf-8')
    results = []

    # 1. MD5
    md5_hash = hashlib.md5(encoded_text).hexdigest()
    results.append({
        "algo": "MD5",
        "hash": md5_hash,
        "status": "🔴 INSECURE - DO NOT USE"
    })

    # 2. SHA-256
    sha256_hash = hashlib.sha256(encoded_text).hexdigest()
    results.append({
        "algo": "SHA-256",
        "hash": sha256_hash,
        "status": "🟡 GOOD FOR INTEGRITY, NOT PASSWORDS"
    })

    # 3. Bcrypt
    if HAS_BCRYPT:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(encoded_text, salt)
        results.append({
            "algo": "Bcrypt",
            "hash": hashed.decode('utf-8'),
            "status": "🟢 BEST PRACTICE (Salted & Slow)"
        })
    else:
        results.append({
            "algo": "Bcrypt",
            "hash": "N/A",
            "status": "⚪ SKIPPED (Install 'bcrypt')"
        })
        
    return results

def generate_hashes(text):
    print(f"\n[*] Hashing input: '{text}'\n")
    results = get_hashes(text)
    
    for r in results:
        print(f"Algorithm: {r['algo']}")
        print(f"Hash: {r['hash']}")
        print(f"Status: {r['status']}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demonstrate different hashing algorithms")
    parser.add_argument("text", help="String to hash")
    args = parser.parse_args()
    
    generate_hashes(args.text)
