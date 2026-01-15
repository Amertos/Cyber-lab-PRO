# Common Cyber Attacks & Defenses

This document explains the theory behind three of the most common web vulnerabilities. Understanding these is the first step to securing code.

---

## 1. SQL Injection (SQLi)

### The Concept
SQL Injection occurs when untrusted user input is concatenated directly into a database query string. An attacker can input malicious SQL commands to manipulate the database.

**Vulnerable Python Code:**
```python
# BAD PRACTICE
user_input = "admin' OR '1'='1"
query = "SELECT * FROM users WHERE username = '" + user_input + "'"
# Resulting Query: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
# This logs the attacker in as admin without a password.
```
### The Solution: Prepared Statements
Never concatenate strings for queries. Use Prepared Statements (also known as Parameterized Queries). The database treats the input strictly as data, not executable code.

**Secure Python Code:**
```python
# GOOD PRACTICE (using sqlite3 or other libraries)
cursor.execute("SELECT * FROM users WHERE username = ?", (user_input,))
```

---

## 2. Cross-Site Scripting (XSS)

### The Concept
XSS happens when an application includes untrusted data in a web page without proper validation or escaping. This allows the attacker to execute malicious scripts (JavaScript) in the victim's browser (e.g., stealing cookies).

**Scenario:**
A blog comment section takes input: `<script>alert('Hacked')</script>` and displays it directly to other users.

### The Solution: Context-Aware Encoding (Sanitization)
Convert special characters into their HTML entity equivalents before rendering.
`<` becomes `&lt;`
`>` becomes `&gt;`

Modern web frameworks (Django, Flask/Jinja2, React) handle this automatically by default.

---

## 3. Man-in-the-Middle (MitM)

### The Concept
An attacker intercepts communication between two parties (User and Server). If the data is sent in plaintext (HTTP), the attacker can read passwords and credit card numbers.

### The Solution: HTTPS / TLS
Transport Layer Security (TLS) encrypts the tunnel between the user and the server. Even if an attacker intercepts the data packets, they look like random garbage characters without the private decryption key.

**Key takeaway:** Never enter sensitive data on a website displaying an "Unsecured" or "http://" warning.
