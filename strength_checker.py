import argparse
import re
import math

def calculate_entropy(password):
    """
    Calculates password entropy (bits of uncertainty).
    Formula: E = Length * log2(Pool_Size)
    """
    pool_size = 0
    if re.search(r'[a-z]', password): pool_size += 26
    if re.search(r'[A-Z]', password): pool_size += 26
    if re.search(r'[0-9]', password): pool_size += 10
    if re.search(r'[^a-zA-Z0-9]', password): pool_size += 32  # Special chars

    if pool_size == 0:
        return 0
    
    return len(password) * math.log2(pool_size)

def analyze_strength(password):
    """
    Returns a dictionary with strength analysis data.
    """
    # 1. Criteria Check
    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))

    # 2. Calculate Entropy
    entropy = calculate_entropy(password)
    
    grade = ""
    advice = ""
    
    if entropy < 28:
        grade = "WEAK 🔴"
        advice = "Immediate change required. Use a passphrase (e.g., 4 random words)."
    elif entropy < 60:
        grade = "MEDIUM 🟡"
        advice = "Decent, but vulnerable to GPU clusters. Add length."
    else:
        grade = "STRONG 🟢"
        advice = "Good job. Ensure this is unique to this account."

    return {
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "entropy": entropy,
        "grade": grade,
        "advice": advice
    }

def check_strength(password):
    """
    CLI Wrapper for analyze_strength
    """
    print(f"\n[*] Analyzing password: '{password}'")
    result = analyze_strength(password)
    
    print(f"[-] Length: {result['length']}")
    print(f"[-] Contains Uppercase: {result['has_upper']}")
    print(f"[-] Contains Lowercase: {result['has_lower']}")
    print(f"[-] Contains Numbers: {result['has_digit']}")
    print(f"[-] Contains Specials: {result['has_special']}")
    print(f"[-] Entropy Score: {result['entropy']:.2f} bits")
    print(f"\n[RESULT] Grade: {result['grade']}")
    print(f"Advice: {result['advice']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Password Strength & Entropy Calculator")
    parser.add_argument("password", help="The password to analyze")
    args = parser.parse_args()
    
    check_strength(args.password)
