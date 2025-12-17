#!/usr/bin/python3
import requests
import re

s = requests.Session()

# 1. Логин (без CSRF)
s.post("http://dvwa.local/login.php",
      data={'username':'admin','password':'password','Login':'Login'})

# 2. Security
s.post("http://dvwa.local/security.php",
      data={'security':'low','seclev_submit':'Submit'})

# 3. Пробуем получить brute force страницу
brute_url = "http://dvwa.local/vulnerabilities/brute/"
r = s.get(brute_url)

print(f"Brute page: {len(r.text)} chars")

# 4. Ищем ВСЕ hidden поля
print("\nSearching for ALL hidden inputs:")
hidden_matches = re.findall(r'<input[^>]*type="hidden"[^>]*>', r.text)
for hidden in hidden_matches:
    print(f"  Found: {hidden}")

# 5. Ищем ЛЮБОЙ токен
token_match = re.search(r'name="([^"]+)" value="([^"]+)"', r.text)
if token_match:
    token_name, token_value = token_match.groups()
    print(f"\nToken found: {token_name} = {token_value}")
    
    # Пробуем с этим токеном
    test_url = f"{brute_url}?username=admin&password=password&Login=Login&{token_name}={token_value}"
    r = s.get(test_url)
    
    if 'Welcome to the password protected area' in r.text:
        print(f"\nSUCCESS with token {token_name}!")
    else:
        print(f"\nFailed even with token")
else:
    print("\nNo tokens found at all")
