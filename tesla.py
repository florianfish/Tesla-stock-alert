import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup
import requests
from decouple import config

urls = {
    #"Rennes": 'https://www.tesla.com/fr_FR/inventory/new/m3?TRIM=LRRWD%2CM3RWD&PAINT=WHITE&arrangeby=plh&zip=35000&range=0',
    #"Nantes": 'https://www.tesla.com/fr_FR/inventory/new/m3?TRIM=LRRWD%2CM3RWD&PAINT=WHITE&arrangeby=plh&zip=44000&range=0',
    "Test": 'https://www.tesla.com/fr_FR/inventory/new/my?PAINT=WHITE&arrangeby=plh&zip=35000&range=200'
}

########################
# Telegram configuration
########################
telegram_chat_id = config("TELEGRAM_CHAT_ID")
telegram_token = config("TELEGRAM_API_TOKEN")

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

for city, url in urls.items():
    try:
        # Configuration du navigateur Chrome
        driver = uc.Chrome(headless=True, use_subprocess=False)
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('article', class_='result card')

        for card in cards:
            modele_libelle, status_libelle = get_basic_info(card)
            purchase_price_libelle = get_price(card)

            if status_libelle == "Véhicule prêt à être livré":
                message_to_send = '[' + city + '] ' + modele_libelle + ' - ' + status_libelle + ' - ' + purchase_price_libelle
                send_telegram_notif(message_to_send)
    finally:
        # Fermer le navigateur après avoir terminé
        driver.quit()