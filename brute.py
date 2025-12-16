#!/usr/bin/python3
import requests

print("TEST 1: Direct login test")
print("="*50)

# 1. Пробуем самый простой вариант
s = requests.Session()

# Пробуем без CSRF токена
r = s.post("http://dvwa.local/login.php", 
           data={'username':'admin','password':'password','Login':'Login'},
           allow_redirects=True)

print(f"Login response status: {r.status_code}")
print(f"Login response URL: {r.url}")
print(f"Login response length: {len(r.text)}")

# Проверяем где мы
if 'login.php' in r.url:
    print("[ERROR] Still on login page - login failed")
else:
    print("[OK] Redirected from login page")

print("\n" + "="*50)
print("TEST 2: Manual cookie test")
print("="*50)

# Попробуем вручную установить PHPSESSID
import http.cookies
import os

# Создаем свои cookies
s.cookies.set('PHPSESSID', 'test123', domain='dvwa.local', path='/')
s.cookies.set('security', 'low', domain='dvwa.local', path='/')

# Пробуем получить brute force страницу
r = s.get("http://dvwa.local/vulnerabilities/brute/")
print(f"Brute page length: {len(r.text)}")
print(f"Brute page preview: {r.text[:150]}")

print("\n" + "="*50)
print("TEST 3: Actual brute force")
print("="*50)

# Попробуем СРАЗУ с правильными параметрами
# В DVWA на low security НЕ НУЖЕН CSRF токен
url = "http://dvwa.local/vulnerabilities/brute/"
params = "?username=admin&password=password&Login=Login"

r = s.get(url + params)
print(f"Test request length: {len(r.text)}")

# Ищем КОНКРЕТНО что в ответе
lines = r.text.split('\n')
for i, line in enumerate(lines):
    if 'Welcome' in line or 'incorrect' in line or 'password' in line.lower():
        print(f"Line {i}: {line.strip()[:80]}")

print("\n" + "="*50)
print("MANUAL CHECK REQUIRED!")
print("="*50)
print("Open Firefox and check:")
print("1. http://dvwa.local/")
print("2. Login: admin / password")
print("3. Go to Brute Force module")
print("4. Try username: admin, password: password")
print("5. What does it say on the page?")
print("   Take screenshot or copy text")
