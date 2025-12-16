#!/usr/bin/python3
import requests
import sys

print("="*50)
print("DVWA CONNECTION TEST")
print("="*50)

# 1. Проверяем доступность DVWA
print("\n[1] Testing connection to DVWA...")
try:
    r = requests.get("http://127.0.0.1", timeout=5)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        print("  [OK] DVWA is accessible")
    else:
        print(f"  [WARNING] Unexpected status: {r.status_code}")
except Exception as e:
    print(f"  [ERROR] Cannot connect: {e}")
    sys.exit(1)

# 2. Проверяем логин
print("\n[2] Testing login...")
s = requests.Session()
try:
    r = s.post("http://127.0.0.1/login.php", 
               data={'username':'admin','password':'password','Login':'Login'},
               timeout=5)
    
    if "Login failed" in r.text:
        print("  [ERROR] Login failed - wrong credentials")
        print("  Try using 'admin' / 'password'")
    else:
        print("  [OK] Login successful (no 'Login failed' message)")
        
except Exception as e:
    print(f"  [ERROR] Login request failed: {e}")

# 3. Проверяем security setting
print("\n[3] Setting security to low...")
try:
    r = s.post("http://127.0.0.1/security.php",
               data={'security':'low','seclev_submit':'Submit'},
               timeout=5)
    print("  [OK] Security level set")
except Exception as e:
    print(f"  [ERROR] Cannot set security: {e}")

# 4. Тест brute force модуля
print("\n[4] Testing brute force module directly...")
print("  Sending: admin / password")

try:
    r = s.get("http://127.0.0.1/vulnerabilities/brute/?username=admin&password=password&Login=Login",
              timeout=5)
    
    print(f"  Response status: {r.status_code}")
    print(f"  Response size: {len(r.text)} chars")
    
    # Ищем КЛЮЧЕВЫЕ СЛОВА которые точно есть
    print("\n  Searching for ANY text in response...")
    
    # Вырежем весь HTML и оставим только текст
    import re
    # Убираем теги
    text_only = re.sub('<[^<]+?>', ' ', r.text)
    # Убираем лишние пробелы
    text_only = ' '.join(text_only.split())
    
    print(f"  Text-only (first 200 chars):")
    print("  " + "-"*40)
    print(f"  {text_only[:200]}")
    print("  " + "-"*40)
    
    # Покажем оригинальный ответ для отладки
    print("\n  [DEBUG] First 500 chars of raw response:")
    print("  " + "-"*40)
    print(r.text[:500])
    print("  " + "-"*40)
    
except Exception as e:
    print(f"  [ERROR] Brute force test failed: {e}")

print("\n" + "="*50)
print("TEST COMPLETE")
print("="*50)
