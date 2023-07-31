import json
import pprint
import time
import threading
import re

from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

import ctypes  # An included library with Python install.

html = None

urls = {
    "Toronto": 'https://www.tesla.com/en_CA/inventory/new/m3?TRIM=SRPRWD,LRAWD,LRAWDP&arrangeby=plh&zip=M3A1C6&range=200',
    "Quebec City" : 'https://www.tesla.com/en_CA/inventory/new/m3?TRIM=SRPRWD,LRAWD,LRAWDP&arrangeby=plh&zip=G1N2G3&range=200',
    "Montreal" : 'https://www.tesla.com/en_CA/inventory/new/m3?TRIM=SRPRWD,LRAWD,LRAWDP&arrangeby=plh&zip=H1K&range=200',
}

results_container_selector = 'div.results-container.results-container--grid.results-container--has-results'
delay = 10  # seconds

priceThreshold = 55990

while True:

    for city in urls:

        try:

            print(datetime.now().strftime("%H:%M:%S") + " Searching Tesla's website in " + city)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            browser = webdriver.Chrome('C:/Users/mmowbray/Desktop/chromedriver.exe', options=chrome_options)
            browser.get(urls[city])

            # wait for results to be displayed
            WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, results_container_selector))
            )

        except TimeoutException:
            print('Loading took too much time!')
        else:
            html = browser.page_source
        finally:
            browser.quit()

        if html:
            soup = BeautifulSoup(html, 'lxml')
            cars = [];
            for car_html in soup.select_one(results_container_selector).findChildren('article'):

                car = {}

                car['price'] = int(re.sub('[^0-9]', '', car_html.select_one('section.result-header').select_one('div.result-pricing').select_one('h3').text.replace('$', '').replace(',', '')))
                car['colour'] = car_html.select('section.result-features.features-grid')[0].select('ul')[1].select('li')[0].text
                car['type'] = car_html.select_one('section.result-header').select_one('div.result-basic-info').select_one('h3').text
                car['trim'] = car_html.select_one('section.result-header').select_one('div.result-basic-info').select('div')[0].text
                car['mileage'] = int(car_html.select_one('section.result-header').select_one('div.result-basic-info').select('div')[1].text.replace('Less than ', '').replace(' km odometer', '').replace(',', ''))
                car['location'] = car_html.select_one('section.result-header').select_one('div.result-basic-info').select('div')[2].text
                car['wheels'] = re.sub('[^0-9]', '', car_html.select('section.result-features.features-grid')[0].select('ul')[1].select('li')[1].text) + " inch wheels"
                car['interior'] = car_html.select('section.result-features.features-grid')[0].select('ul')[1].select('li')[2].text

                if(car['price'] < priceThreshold):
                    cars.append(car)
                    threading.Thread(target=Mbox, args=('YOUR TESLA IS READY', 'There is a Tesla for sale for in ' + str(car['location']) + "\n\n Details: \n\n " + json.dumps(car), 1)).start()
                    print("FOUND A CAR for " + str(car['price']) + "$ in " + city)

            time.sleep(30) # seconds
