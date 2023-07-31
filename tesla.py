import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup
import requests
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import urllib.parse

urls = {
    "Rennes": 'https://www.tesla.com/fr_FR/inventory/new/m3?TRIM=LRRWD%2CM3RWD&PAINT=WHITE&arrangeby=plh&zip=35000&range=200',
    #"Test": 'https://www.tesla.com/fr_FR/inventory/new/my?PAINT=WHITE&arrangeby=plh&zip=35000&range=200'
}

modeles = {
    "222": "LRWY222", # Model Y Propulsion
    "218": "XP7Y218", # Model Y Grande Autonomie, Transmission intégrale Dual Motor
    "228":"LRW3228", # Model 3 Propulsion & Model 3 Grande Autonomie, Propulsion
}

########################
# Telegram configuration
########################
telegram_chat_id = config("TELEGRAM_CHAT_ID")
telegram_token = config("TELEGRAM_API_TOKEN")

def get_html_source(url, wait_time=20):
    try:
        # Configurer les options de Chrome (ajoutez '--headless' si vous voulez exécuter en mode sans tête)
        options = Options()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))
        options.add_argument('--headless')

        # Initialiser le navigateur Chrome
        driver = webdriver.Chrome(options=options)

        # Attendre que la page soit complètement chargée (modifier le délai selon vos besoins)
        wait = WebDriverWait(driver, 20)

        # Charger la page
        driver.get(url)

        # Attendre que le contenu de la page soit complètement chargé
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'results-container--has-results')))

        # Récupérer le code HTML complet de la page
        html_content = driver.page_source

        # Fermer le navigateur
        driver.quit()

        return html_content

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None

# Fonction pour récupérer les informations basiques d'une card (= voiture)
def get_basic_info(card):
    infos_basic = card.find('div', class_='result-basic-info')
    modele = infos_basic.find('div', class_='tds-text_color--10').get_text()
    status = infos_basic.find('div', class_='tds-text--caption').get_text()
    return modele, status

# Fonction pour récupérer le prix d'une card (= voiture
def get_price(card):
    price = card.find('div', class_='result-price')
    purchase_price = price.find('span', class_='result-purchase-price tds-text--h4').get_text()
    return purchase_price

# Fonction pour envoyer une notif Telegram
def send_telegram_notif(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={message}"
    requests.post(url)


#print(get_data_id_from_article('<article class="result card" data-id="234_878a18cf9846793b241c7a02d1f511ad-search-result-container"><section class="result-header"></article>'))

for city, url in urls.items():
    try:
        html = get_html_source(url)
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('article', class_='result card')
        notifSent = False
        for card in cards:
            modele_libelle, status_libelle = get_basic_info(card)
            purchase_price_libelle = get_price(card)
            
            message = '[' + city + '] ' + modele_libelle + ' - ' + status_libelle + ' - ' + purchase_price_libelle
            
            print(message)
            if status_libelle == "Véhicule prêt à être livré":
                message_to_send = '[' + city + '] ' + modele_libelle + ' - ' + status_libelle + ' - ' + purchase_price_libelle
                send_telegram_notif(message_to_send)
                notifSent = True
        if notifSent is True:
            send_telegram_notif(urllib.parse.quote(url))
    finally:
        print('ended')