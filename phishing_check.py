import argparse
import re

def get_phishing_score(text):
    score = 0
    findings = []

    # 1. Suspicious Keywords
    keywords = {
        "urgent": 20, "verify": 15, "account suspended": 30,
        "act now": 20, "bank": 10, "password": 10,
        "ssn": 50, "winner": 20
    }

    text_lower = text.lower()
    for word, points in keywords.items():
        if word in text_lower:
            score += points
            findings.append(f"Keyword: '{word}' (+{points})")

    # 2. IP Address check
    ip_regex = r"https?://(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
    if re.search(ip_regex, text):
        score += 50
        findings.append("Raw IP address in URL (+50)")

    # 3. Generic Greetings
    if re.search(r"dear customer|dear user", text_lower):
        score += 10
        findings.append("Generic greeting detected (+10)")
        
    risk_level = "Low Risk 🟢"
    if score >= 50:
        risk_level = "High Risk 🔴"
    elif score >= 20:
        risk_level = "Medium Risk 🟡"

    return {
        "score": score,
        "findings": findings,
        "risk_level": risk_level
    }

def analyze_text(text):
    print("\n[*] Analyzing text for phishing indicators...\n")
    result = get_phishing_score(text)
    
    if not result['findings']:
        print("No obvious indicators found.")
    else:
        for f in result['findings']:
            print(f"[-] {f}")
    
    print(f"\nTotal Suspicion Score: {result['score']}")
    print(f"[RESULT] {result['risk_level']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Phishing Content Scanner")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text", help="Text string to analyze")
    group.add_argument("-f", "--file", help="Path to text file containing email body")
    
    args = parser.parse_args()
    
    content = ""
    if args.text:
        content = args.text
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print("Error: File not found.")
            exit()
            
    analyze_text(content)
