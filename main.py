from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker
from colorama import Fore as F, Style, init
import random
import os
import time

init(autoreset=True)

CONFIG = {
    "domain"   : "chsangkara.com",
    "password" : "@Sangkara123"
}

os.system('cls' if os.name == "nt" else 'clear')
amount = int(input("How many? (1 - 100) : "))

proxy_auth_plugin_path = 'proxy_auth_plugin.zip'
options = webdriver.ChromeOptions()
options.add_extension(proxy_auth_plugin_path)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=400,400")
options.add_argument("--log-level=3")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
# options.add_argument("--headless") #not work , check compatible your chrome version

try:    
    driver = webdriver.Chrome(options=options)
    time.sleep(3)
    os.system('cls' if os.name == "nt" else 'clear')
    print(F'''
{Style.BRIGHT}   ___                      
  / _ \__ _ _   _  ___ ___  
 / /_)/ _` | | | |/ __/ _ \ 
/ ___/ (_| | |_| | (_| (_) |    {Style.BRIGHT}{F.RED}Unlimited create{F.RESET}
\/    \__,_|\__, |\___\___/     t.me/chsangkara
            |___/           
    ''')
    success_count = 1
    while success_count < amount:
        try:
            driver.get("http://chsangkara.my.id/bot/payco")
            email = Faker().first_name().lower() + Faker().last_name().lower() + str(random.randint(100, 999)) + "@" + CONFIG['domain']
            password = CONFIG['password']
            
            while True:
                email_input = driver.find_element(By.CSS_SELECTOR, '#emailId')
                password_input = driver.find_element(By.CSS_SELECTOR, '#password')
                email_input.send_keys(email)
                password_input.send_keys(password)
                confirm_button = driver.find_element(By.CSS_SELECTOR, "#confirmButton")
                confirm_button.click()
                break
            
            print(f"\n{Style.BRIGHT}[Information User {success_count}]\nEmail    : {F.GREEN}{email}\n{F.RESET}Password : {F.YELLOW}{password}")
            
            while True:
                inner_text = driver.execute_script("return document.body.innerHTML")
                if "회원 가입이 완료되었어요!" in inner_text:
                    with open("payco.txt", "a") as f:
                        f.write(f"{email} | {password}\n")
                    print(f"{Style.BRIGHT}Saved    : {F.GREEN}payco.txt !")
                    success_count += 1
                    break
                else:
                    print(f"{Style.DIM}{F.RED}Failed to register")
                    break
        except Exception as e:
            continue

        driver.execute_script("window.open('');")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
