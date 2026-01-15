import os

def shred_file(path):
    try:
        if not os.path.isfile(path): return "Error: Not a file"
        size = os.path.getsize(path)
        with open(path, "ba+", buffering=0) as f:
            for _ in range(3):
                f.seek(0); f.write(os.urandom(size)); os.fsync(f.fileno())
        os.remove(path)
        return "Success: File shredded."
    except Exception as e: return f"Error: {e}"
