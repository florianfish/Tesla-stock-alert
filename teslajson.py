import requests
from decouple import config
import sys


########################
# VARIABLES
########################
PRICE_LIMIT = 39000
# Récupérer les arguments passés via la ligne de commande
print_all_results = False  # Valeur par défaut, si le paramètre n'est pas passé

if len(sys.argv) > 1:
    parametre = sys.argv[1]
    if parametre.lower() in ["true", "1"]:
        print_all_results = True

########################
# Telegram configuration
########################
telegram_chat_id = config("TELEGRAM_CHAT_ID")
telegram_token = config("TELEGRAM_API_TOKEN")

urls = {
    "35000": 'https://www.tesla.com/inventory/api/v1/inventory-results?query=%7B%22query%22%3A%7B%22model%22%3A%22m3%22%2C%22condition%22%3A%22new%22%2C%22options%22%3A%7B%22TRIM%22%3A%5B%22LRRWD%22%2C%22M3RWD%22%5D%2C%22PAINT%22%3A%5B%22GRAY%22%2C%22WHITE%22%2C%22BLUE%22%5D%7D%2C%22arrangeby%22%3A%22Price%22%2C%22order%22%3A%22asc%22%2C%22market%22%3A%22FR%22%2C%22language%22%3A%22fr%22%2C%22super_region%22%3A%22north%20america%22%2C%22lng%22%3A-1.7075198%2C%22lat%22%3A48.11734209999999%2C%22zip%22%3A%2244000%22%2C%22range%22%3A50%2C%22region%22%3A%22FR%22%7D%2C%22offset%22%3A0%2C%22count%22%3A50%2C%22outsideOffset%22%3A0%2C%22outsideSearch%22%3Afalse%7D',
    "44000": 'https://www.tesla.com/inventory/api/v1/inventory-results?query=%7B%22query%22%3A%7B%22model%22%3A%22m3%22%2C%22condition%22%3A%22new%22%2C%22options%22%3A%7B%22TRIM%22%3A%5B%22LRRWD%22%2C%22M3RWD%22%5D%2C%22PAINT%22%3A%5B%22GRAY%22%2C%22WHITE%22%2C%22BLUE%22%5D%7D%2C%22arrangeby%22%3A%22Price%22%2C%22order%22%3A%22asc%22%2C%22market%22%3A%22FR%22%2C%22language%22%3A%22fr%22%2C%22super_region%22%3A%22north%20america%22%2C%22lng%22%3A-1.7075198%2C%22lat%22%3A48.11734209999999%2C%22zip%22%3A%2244000%22%2C%22range%22%3A50%2C%22region%22%3A%22FR%22%7D%2C%22offset%22%3A0%2C%22count%22%3A50%2C%22outsideOffset%22%3A0%2C%22outsideSearch%22%3Afalse%7D',
}
# Fonction pour envoyer une notif Telegram
def send_telegram_notif(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={telegram_chat_id}&text={message}&disable_web_page_preview=true"
    requests.post(url)

for zipcode, url in urls.items():
    print(f"::::::::::::::::::::")
    print(f":: {zipcode} ::")
    print(f"::::::::::::::::::::")
    message_all_results = "[" + zipcode + "]\n\n"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        vehicles = data.get("results", [])
        match = False
        for vehicle in vehicles:
            hash = vehicle.get("Hash", "")
            vin = vehicle.get("VIN", "")
            trim_name = vehicle.get("TrimName", "")
            paint = vehicle.get("PAINT", "")
            in_transit = vehicle.get("InTransit", False)
            is_demo = bool(vehicle.get("IsDemo", False))
            is_at_location = bool(vehicle.get("IsAtLocation", False))
            country_has_vehicle_at_location = vehicle.get("CountryHasVehicleAtLocation", "")
            country_code = vehicle.get("CountryCode", "")
            discount = vehicle.get("Discount", 0)
            inventory_price = int(vehicle.get("InventoryPrice", 0) / 10)
            total_price = vehicle.get("TotalPrice", 0)
            link = "https://www.tesla.com/fr_FR/m3/order/" + vin + "?postal=" + zipcode

            if inventory_price <= PRICE_LIMIT and is_at_location is True and is_demo is False:
                match = True
                message = f"{trim_name} à {inventory_price} €, {paint} >> {link}"
                send_telegram_notif(message)
            if print_all_results is True:
                message_all_results = message_all_results + trim_name + " à " + str(inventory_price) + " €, Couleur {paint}, En transit = " + str(in_transit) + ", Démonstration = " + str(is_demo) + " (" + link + ")\n"
        if match is False:
            print("Aucun résultat :'(")
    else:
        print(f"Error!")

    if print_all_results is True and zipcode == "35000":
        print(message_all_results)
        send_telegram_notif(message_all_results)

