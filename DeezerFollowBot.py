import threading
import requests
import random
import string
import time
from datetime import datetime, timedelta

# Load proxies from file
with open("proxies.txt", "r") as f:
    proxy_list = [line.strip() for line in f if line.strip()]

def get_random_proxy():
    proxy = random.choice(proxy_list)
    return {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(6, 12)))
    domain = random.choice(domains)
    return f"{username}@{domain}"

def generate_random_birthdate():
    end_date = datetime.now() - timedelta(days=365*18)
    start_date = end_date - timedelta(days=365*12)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")

def follow_user(session_token, user_id):
    follow_url = "https://api.deezer.com/1.0/gateway.php?api_key=4VCYIJUCDLOUELGD1V8WBVYBNVDYOXEWSLLZDONGBBDFVXTZJRXPR29JRLQFO6ZE&sid=frb6499eca2a89877e3c72ffee2c443498a52786&method=friend.follow&output=3&input=3"
    
    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "api.deezer.com",
        "User-Agent": "Deezer/8.0.37.6 (Android; 9; Mobile; us) samsung SM-N975F"
    }

    params = {
        "network": "f3137a132d8b00c54b6fc655041ee025ee8192cb20b98f3ffdb2c35673cafc6f",
        "arl": session_token
    }

    data = {"friend_id": user_id}

    try:
        response = requests.post(follow_url, headers=headers, params=params, json=data, proxies=get_random_proxy(), timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('results') is True:
                return True
    except Exception as e:
        pass
    return False

def register_deezer_account(user_id):
    register_url = "https://api.deezer.com/1.0/gateway.php?api_key=4VCYIJUCDLOUELGD1V8WBVYBNVDYOXEWSLLZDONGBBDFVXTZJRXPR29JRLQFO6ZE&sid=frb6499eca2a89877e3c72ffee2c443498a52786&method=user_create&output=3&input=3"

    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "api.deezer.com",
        "User-Agent": "Deezer/8.0.37.6 (Android; 9; Mobile; us) samsung SM-N975F"
    }

    params = {
        "network": "f3137a132d8b00c54b6fc655041ee025ee8192cb20b98f3ffdb2c35673cafc6f"
    }

    email = generate_random_email()
    birthdate = generate_random_birthdate()
    sex = random.choice(["M", "F"])

    data = {
        "EMAIL": email,
        "PASSWORD": "881137f666472f3affc53976c3b15d5d",
        "BLOG_NAME": "",
        "BIRTHDAY": birthdate,
        "SEX": sex,
        "EXPLICIT_ALLOW_TRANSFER_DATA_TO_FRANCE": False,
        "lang": "us",
        "recaptcha": "x"
    }

    try:
        response = requests.post(register_url, headers=headers, params=params, json=data, proxies=get_random_proxy(), timeout=10)
        response_data = response.json()
        
        if response.status_code == 200:
            token = response_data.get('results', '')
            if token:
                account_info = f"{email}:asdasd123! | Token: {token}\n"
                with open("created.txt", "a") as f:
                    f.write(account_info)
                print(f"Success! Account created: {email}:asdasd123! | Token: {token}")
                
                if follow_user(token, user_id):
                    print("User followed successfully!")
    except Exception as e:
        pass

def run_forever(user_id):
    while True:
        register_deezer_account(user_id)

if __name__ == "__main__":
    user_id = input("Enter the user ID to follow: ").strip()
    
    threads = []
    for _ in range(100):
        t = threading.Thread(target=run_forever, args=(user_id,))
        t.daemon = True
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
