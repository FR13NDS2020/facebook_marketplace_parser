import pickle
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import keyboard

url = "https://www.facebook.com/marketplace/"
# options
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument(argument=f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

options.headless = False
service = Service(r'\chromedriver\chromedriver.exe')

driver = webdriver.Chrome(service=service, options=options)


def login(login, password):
    allow_cookie = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]')
    allow_cookie.click()

    email = driver.find_element(By.NAME, "email")
    email.send_keys(login)

    passwd = driver.find_element(By.NAME, "pass")
    passwd.send_keys(password)
    passwd.send_keys("\ue007")


def main():

    account_name = input("input the account name: ")
    driver.get(url=url)
    print("you can enter the data manually or enter the data in the console")
    log = input("enter your login or 0 if you entered the data yourself: ")
    if log == "0":
        print(r"when you log in to your account, press about 3 sec 'f' ")
        while not keyboard.is_pressed('f'):
            time.sleep(3)

    else:
        pas = input("input the password: ")
        login(log, pas)

    pickle.dump(driver.get_cookies(), open(account_name, "wb"))


if __name__ == "__main__":
    main()