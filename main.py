import threading
import keyboard
from bs4 import BeautifulSoup as bs
import pickle
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from visualize import visualize
import sys


url = "https://www.facebook.com/marketplace/"
# options
options = webdriver.ChromeOptions()
caps = DesiredCapabilities().CHROME
caps["javascriptEnabled"] = False

options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-background-networking')
options.add_argument('--disable-extensions')
options.add_argument('--disable-infobars')
options.add_argument('--no-sandbox')
options.add_argument('--disable-features=BackgroundSyncService,AsyncDns,AsyncFrameScrolling,AsyncResourcePrefetch,AudioServiceOutOfProcess')
options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation', 'disable-extensions', 'disable-ftp', 'disable-http2', 'disable-ipc-flooding-protection', 'disable-background-networking', 'disable-background-timer-throttling'])


options.add_argument("--disable-notifications")
options.add_argument(argument=f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--blink-settings=imagesEnabled=false")
# options.page_load_strategy = 'eager'
options.add_argument("--disk-cache-size=1048576")
options.headless = True
service = Service(r'\chromedriver\chromedriver.exe')


driver = webdriver.Chrome(service=service, options=options, desired_capabilities=caps)
driver.execute_cdp_cmd('Network.setBlockedURLs', {"urls": ["*://*.xhr"]})


def clean_links(data):
    cleaned_data = []
    for item in data:
        cleaned_link = item['link'].split('?')[0]

        if '€' in item['price']:
            price = item['price'].split('€')[1]  # get the first price only
            price = "€ " + price.strip()
        else:
            price = item['price']
        cleaned_item = {
            "link": cleaned_link,
            "price": price,
            "title": item["title"],
            "location": item["location"]
        }
        cleaned_data.append(cleaned_item)

    with open("data.json", "w", encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
    return cleaned_data


def parsing(source):
    items = []
    soup = bs(source, "lxml")
    main_div = soup.find("div", {"class": "xkrivgy x1gryazu x1n2onr6" or "x8gbvx8 x78zum5 x1q0g3np x1a02dak x1rdy4ex xcud41i x4vbgl9 x139jcc6 x1nhvcw1"})
    try:
        all = main_div.findAll("div", {
        "class": "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e xnpuxes x291uyu x1uepa24 x1iorvi4 xjkvuk6"})
        for i in all:
            link = i.find("a")
            if link and link["href"].startswith("/"):
                link = link["href"]
                price = i.find("div", {"class": "x78zum5 x1q0g3np x1iorvi4 x4uap5 xjkvuk6 xkhd6sd"})
                price = price.text if price else ""
                title = i.find("div", {"class": "xyqdw3p x4uap5 xjkvuk6 xkhd6sd"})
                title = title.text if title else ""
                location = i.find("div", {"class": "x1iorvi4 x4uap5 xjkvuk6 xkhd6sd"})
                location = location.text if location else ""
                data = {"link": link, "price": price, "title": title, "location": location}
                items.append(data)
    except Exception as ex:
        print(ex)

    return items


def check():
    divs2 = len(driver.find_elements(By.CSS_SELECTOR, 'div.x8gbvx8.x78zum5.x1q0g3np.x1a02dak.x1rdy4ex.xcud41i.x4vbgl9.x139jcc6.x1nhvcw1, div.xkrivgy.x1gryazu.x1n2onr6'))

    return divs2


def scroll(url, account_name):
    try:
        driver.get(url=url)
        # logging in and getting cookies
        time.sleep(2)
        try:
            allow_cookie = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]')
            allow_cookie.click()
        except:
            print("cookie check not found")

        for cookie in pickle.load(open(account_name, "rb")):
            driver.add_cookie(cookie)

        driver.refresh()
        driver.get(url)

        while check() == 2 and not keyboard.is_pressed('q'):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    except Exception as ex:
        print(ex)


def spinner(stop_event):
    frames = ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(frames[i])
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write('\b\b\b')
        i = (i + 1) % len(frames)
    # clear the spinner animation before exiting
    sys.stdout.write('\b\b\b   \b\b\b')
    sys.stdout.flush()


def main():
    account = input("print account name: ")
    url = input("insert the link for parsing somethin like ('https://www.facebook.com/marketplace/category/hobbies'): ")
    print("you can click on the 'q' button if you want to stop the parser")

    start_time = time.time()
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()

    scroll(url, account)
    data = clean_links(parsing(driver.page_source))
    elapsed_time = time.time() - start_time
    print("Time elapsed for scraping: " + str(elapsed_time))
    stop_event.set()  # set the flag to stop the spinner thread
    spinner_thread.join()
    driver.quit()
    print(str(len(data)) + " items parsed")
    visual = input("if you want to visualize the data print 1: ")
    if visual == "1":
        visualize("data.json", "title")


if __name__ == "__main__":
    main()