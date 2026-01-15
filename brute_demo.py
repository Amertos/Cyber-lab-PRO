import argparse
import time

def attempt_login(guess, attempt_count, target_password, delay=1, log_callback=None):
    """
    Simulates a login attempt with artificial network delay.
    """
    msg = f"[{attempt_count}] Trying password: '{guess}'..."
    if log_callback:
        log_callback(msg)
    else:
        print(msg)
    
    if delay > 0:
        time.sleep(delay) 
    
    if guess == target_password:
        return True
    return False

def run_simulation(wordlist_path=None, single_guess=None, target_password="secret123", max_attempts=5, delay=1, log_callback=None):
    if not log_callback:
        def simple_print(x): print(x)
        log_callback = simple_print

    log_callback("[*] Starting Brute Force Simulation")
    log_callback("[*] Target Account: admin")
    log_callback(f"[*] Target Password (DEMO): {target_password}")
    log_callback(f"[*] Defense Protocol: Lockout after {max_attempts} attempts\n")
    
    attempts = 0
    
    # Mode 1: Single Guess
    if single_guess:
        attempts += 1
        success = attempt_login(single_guess, attempts, target_password, log_callback)
        if success:
            log_callback("\n[SUCCESS] Password cracked! Access Granted.")
        else:
            log_callback("\n[FAILED] Incorrect password.")
        return

    # Mode 2: Wordlist Attack
    try:
        # If passed from GUI, 'wordlist_path' might be the actual list of words
        if isinstance(wordlist_path, list):
            lines = wordlist_path
        else:
            with open(wordlist_path, 'r', encoding='latin-1') as f:
                lines = f.readlines()

        for line in lines:
            if attempts >= max_attempts:
                log_callback(f"\n[!!!] ACCOUNT LOCKED - Rate Limiting Active.")
                log_callback("Explain: This prevents attackers from guessing thousands of passwords/second.")
                return

            password_guess = line.strip()
            attempts += 1
            
            if attempt_login(password_guess, attempts, target_password, delay, log_callback):
                log_callback(f"\n[SUCCESS] Password found: '{password_guess}'")
                return
            
        log_callback("\n[FAILED] Password not found in wordlist.")
            
    except Exception as e:
        log_callback(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Educational Brute Force Simulator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-w", "--wordlist", help="Path to password wordlist")
    group.add_argument("-g", "--guess", help="Single password guess")
    parser.add_argument("-t", "--target", default="secret123", help="Target password")
    parser.add_argument("-m", "--max", type=int, default=5, help="Max attempts")
    
    args = parser.parse_args()
    run_simulation(wordlist_path=args.wordlist, single_guess=args.guess, target_password=args.target, max_attempts=args.max)
