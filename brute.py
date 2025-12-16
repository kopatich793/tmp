#!/usr/bin/python3
import requests

print("DVWA BRUTEFORCE - SIMPLE VERSION")
print("="*50)

s = requests.Session()

# 1. Просто логинимся БЕЗ CSRF
print("[1] Logging in...")
r = s.post("http://dvwa.local/login.php",
          data={'username':'admin','password':'password','Login':'Login'})

print(f"Login status: {r.status_code}")
print(f"Response size: {len(r.text)} chars")

# Проверяем куки
print(f"Cookies: {dict(s.cookies)}")

# 2. Пробуем получить brute force страницу
print("\n[2] Accessing brute force page...")
r = s.get("http://dvwa.local/vulnerabilities/brute/")
print(f"Brute page size: {len(r.text)} chars")

# 3. ПРОБУЕМ ПАРОЛЬ
print("\n[3] Testing password...")
test_url = "http://dvwa.local/vulnerabilities/brute/?username=admin&password=password&Login=Login"
r = s.get(test_url)

print(f"Test response: {len(r.text)} chars")

# ВЫВЕДЕМ ВЕСЬ ТЕКСТ БЕЗ HTML
import re
text_only = re.sub('<[^>]+>', ' ', r.text)
text_only = ' '.join(text_only.split())

print("\n" + "="*50)
print("TEXT CONTENT OF PAGE:")
print("="*50)
print(text_only[:500])
print("="*50)

# 4. Если не ясно - сохраним HTML
with open('test.html', 'w') as f:
    f.write(r.text)
print("\nFull HTML saved to: test.html")

# 5. Ищем КЛЮЧЕВЫЕ СЛОВА
print("\n[4] Searching for keywords...")
keywords = ['Welcome', 'incorrect', 'error', 'success', 'protected', 'area', 'login', 'password']
for word in keywords:
    if word.lower() in r.text.lower():
        print(f"Found '{word}' in response")
