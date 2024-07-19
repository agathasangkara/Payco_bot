from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from colorama import Fore as F, Style, init
import random
import os
import time
import requests as r

init(autoreset=True)

CONFIG = {
    "password": "@Sangkara123",
    "Proxy_ZIP": "proxy_auth_plugin.zip"
}

class Email:
    
    def __init__(self):
        self.session = r.Session()
    
    def create_account(self):
        while True:
            try:
                domain = self.session.get("https://api.mail.tm/domains").json()['hydra:member'][0]['domain']
                user = Faker("ID_id").first_name().lower() + Faker("ID_id").last_name().lower() + str(random.randint(10,99))
                email = user + "@" + domain
                data = {
                    "address": email,
                    "password": CONFIG['password']
                }
                create_user = self.session.post(
                    "https://api.mail.tm/accounts",
                    headers={"Content-Type": "application/json"},
                    json=data
                ).status_code
                if create_user == 201:
                    return email
                else:
                    continue
            except Exception as e:
                print(str(e))
                continue
    
    def verify_email(self, email, password: str) -> bool:
        print("\nProccessing email verification")
        data = {
            "address": email,
            "password": password
        }
        try:
            token = self.session.post(
                "https://api.mail.tm/token",
                headers={"Content-Type": "application/json"},
                json=data
            ).json().get('token')

            if token is None:
                print(F.RED + "Failed to get token")
                return False

            print(F.GREEN + "Login email successfully")
            while True:
                cek = self.session.get(
                    "https://api.mail.tm/messages?page=1",
                    headers={"authorization": f"Bearer {token}", "User-Agent": "Mozilla/5.0"}
                )
                if "PAYCO" in cek.text:
                    msgid = cek.json()['hydra:member'][0]['id']
                    verify = self.session.get(
                        f"https://api.mail.tm/messages/{msgid}",
                        headers={"authorization": f"Bearer {token}", "User-Agent": "Mozilla/5.0"}
                    ).json()['text'].split('[')[4].split(']')[0]
                    verify_response = self.session.get(verify).text
                    if "이메일 인증이 완료되었습니다" in verify_response:
                        print(F.GREEN + "Email verified successfully")
                        return True
                else:
                    continue
        except Exception as e:
            print(F.RED + str(e))
            return False

options = webdriver.ChromeOptions()

os.system('cls' if os.name == "nt" else 'clear')
amount = int(input("How many? (1 - 100) : "))
ex = int(input("\n1. Proxies (Use Proxy Extension)\n2. Proxyless (Without Proxy)\n\nChoose : "))
if ex == 1:
    proxy_auth_plugin_path = CONFIG['Proxy_ZIP']
    options.add_extension(proxy_auth_plugin_path)
    
options.add_argument("--disable-gpu")
options.add_argument("--window-size=400,400")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
# options.add_argument("--headless") #not work , check compatible your chrome version using proxies

try:
    driver = webdriver.Chrome(options=options)
    time.sleep(3)
    os.system('cls' if os.name == "nt" else 'clear')
    print(F'''
{Style.BRIGHT}   ___                      
  / _ \\__ _ _   _  ___ ___  
 / /_)/ _` | | | |/ __/ _ \\ 
/ ___/ (_| | |_| | (_| (_) |    {Style.BRIGHT}{F.RED}Unlimited create{F.RESET}
\\/    \\__,_|\\__, |\\___\\___/     t.me/chsangkara
            |___/           
    ''')
    success_count = 0

    while success_count < amount:
        try:
            driver.get("http://chsangkara.my.id/bot/payco")
            email = Email().create_account()
            password = CONFIG['password']
            print(Style.BRIGHT + "\nWaiting loading full page Payco")
            while True:
                try:
                    email_input = driver.find_element(By.CSS_SELECTOR, '#emailId')
                    password_input = driver.find_element(By.CSS_SELECTOR, '#password')
                    confirm_button = driver.find_element(By.CSS_SELECTOR, '#confirmButton')
                    email_input.send_keys(email)
                    time.sleep(1)
                    break
                except Exception as e:
                    inner_text = driver.execute_script("return document.body.innerHTML")
                    if "안전한 이용을 위해 자동 입력 방지 문자를 입력해 주세요." in inner_text:
                        exit(Style.BRIGHT + F.RED + "CAPTCHA detected. Program terminated.")
                    else:
                        continue

            password_input.send_keys(password)
            confirm_button.click()
            
            print(f"\n{Style.BRIGHT}[Information User {success_count + 1}]\nEmail    : {F.GREEN}{email}\n{F.RESET}Password : {F.YELLOW}{password}")
            WebDriverWait(driver, 10).until(lambda driver: "회원 가입이 완료되었어요!" in driver.page_source)

            print(f"{Style.BRIGHT}Status   : {F.GREEN}payco.txt !")
            driver.execute_script("window.open('');")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            if Email().verify_email(email, password):
                success_count += 1
                print(f"{Style.BRIGHT}Successfully created Payco")
                with open("payco.txt", "a") as f:
                    f.write(f"{email} | {password}\n")
            else:
                print(F.RED + "Verification failed.")
                with open("unverifpayco.txt", "a") as f:
                    f.write(f"{email} | {password}\n")
            
        except Exception as e:
            driver.execute_script("window.open('');")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

finally:
    driver.quit()
