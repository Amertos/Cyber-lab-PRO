import hashlib

def crack_md5(target_hash, wordlist):
    """
    Attempts to crack an MD5 hash using a wordlist.
    """
    for word in wordlist:
        if hashlib.md5(word.strip().encode()).hexdigest() == target_hash:
            return f"Found: {word}"
    return "Not found in wordlist."
