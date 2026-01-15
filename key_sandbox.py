import time

class KeySandbox:
    def __init__(self): self.logs = []
    def log_key(self, char): self.logs.append(f"[{time.strftime('%H:%M:%S')}] Key: {char}")
    def get_logs(self): return "\n".join(self.logs[-15:])
