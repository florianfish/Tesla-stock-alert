import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup

urls = {
    "Rennes": 'https://www.tesla.com/fr_FR/inventory/new/m3?TRIM=LRRWD%2CM3RWD&PAINT=WHITE&arrangeby=plh&zip=35000&range=0',
    "Nantes": 'https://www.tesla.com/fr_FR/inventory/new/m3?TRIM=LRRWD%2CM3RWD&PAINT=WHITE&arrangeby=plh&zip=44000&range=0'
}

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

for city, url in urls.items():
    try:
        # Configuration du navigateur Chrome
        driver = uc.Chrome(headless=True, use_subprocess=False)
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        cards = soup.find_all('article', class_='result card')

        nombre = len(cards)
        print("Nombre de véhicules à " + city + " :", nombre)

        for card in cards:
            modele_libelle, status_libelle = get_basic_info(card)
            purchase_price_libelle = get_price(card)

            print('- ' + modele_libelle + ' - ' + status_libelle + ' - ' + purchase_price_libelle)

    finally:
        # Fermer le navigateur après avoir terminé
        driver.quit()
