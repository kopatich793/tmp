#!/usr/bin/python3
import requests

print("TEST START")

# 1. Простой тест без сессии
url = "http://dvwa.local/vulnerabilities/brute/?username=admin&password=password&Login=Login"
r = requests.get(url)
print(f"Direct test: {len(r.text)} chars")

# 2. Проверяем что на странице
if 'Welcome to the password protected area' in r.text:
    print("SUCCESS! No login needed!")
    exit()

# 3. Если нет - пробуем с ручными cookies
print("\nTrying with manual cookies...")
cookies = {
    'PHPSESSID': 'test123',  # Попробуем любой
    'security': 'low'
}

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'http://dvwa.local/vulnerabilities/brute/'
}

r = requests.get(url, cookies=cookies, headers=headers)
print(f"With cookies: {len(r.text)} chars")

# 4. Выводим ВЕСЬ ответ
print("\n=== FULL RESPONSE ===")
print(r.text)
print("=== END ===")

# 5. Команда для ручной проверки
print("\nRUN THIS COMMAND:")
print("curl -v 'http://dvwa.local/vulnerabilities/brute/?username=admin&password=password&Login=Login'")
