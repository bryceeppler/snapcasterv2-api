from re import I
from unittest import result
from bs4 import BeautifulSoup
import requests
import json
from .Scraper import Scraper

class MagicStrongholdScraper(Scraper):
    """
    Magic Stronghold uses a completely exposed API to get the stock of cards
    We can literally hit the API and get all the information we need

    https://api.conductcommerce.com/v1/advancedSearch


    Split cards can be searched using "//" as a split

    """
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.siteUrl = 'https://www.magicstronghold.com'
        self.url = "https://api.conductcommerce.com/v1/advancedSearch"
        self.website = 'magicstronghold'

    def scrape(self):
        # get the json data from this curl request
        # curl 'https://api.conductcommerce.com/v1/advancedSearch' \
        #   -H 'authority: api.conductcommerce.com' \
        #   -H 'accept: application/json, text/javascript, */*; q=0.01' \
        #   -H 'accept-language: en-US,en;q=0.9' \
        #   -H 'cache-control: no-cache' \
        #   -H 'content-type: text/plain' \
        #   -H 'origin: https://www.magicstronghold.com' \
        #   -H 'pragma: no-cache' \
        #   -H 'referer: https://www.magicstronghold.com/' \
        #   -H 'sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"' \
        #   -H 'sec-ch-ua-mobile: ?0' \
        #   -H 'sec-ch-ua-platform: "macOS"' \
        #   -H 'sec-fetch-dest: empty' \
        #   -H 'sec-fetch-mode: cors' \
        #   -H 'sec-fetch-site: cross-site' \
        #   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36' \
        #   --data-raw $'{"productTypeID":1,"name":"elspeth, sun\'s champion","host":"www.magicstronghold.com"}' \
        #   --compressed
        
        response = requests.post(self.url, 
            json={
                "productTypeID": 1,
                "name": self.cardName,
                "host": "www.magicstronghold.com"
            }, 
            headers={
                "authority": "api.conductcommerce.com",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "content-type": "text/plain",
                "origin": "https://www.magicstronghold.com",
                "pragma": "no-cache",
                "referer": "https://www.magicstronghold.com/",
                "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
            })
        # Load the response
        data = json.loads(response.text)

        # The image uri prefix
        imagePrefix = 'https://conduct-catalog-images.s3-us-west-2.amazonaws.com/small/'
        
        # iterate over each card
        for card in data['result']['listings']:
            # get the name of the card
            name = card['inventoryName']
            # foil status is in the card name as '- Foil' tag
            foil = False
            if ' - Foil' in name:
                foil = True
                name.replace(' - Foil', '')

            # sometimes there are other tags like "Card Name - Extended Art"
            # we want to remove the tag from the card name
            if ' - ' in name:
                name = name.split(' - ')[0]
            
            # there can even be more tags like "Card Name (M21)"
            # we want to remove the tag from the card name
            if ' (' in name:
                name = name.split(' (')[0]
                

            setName = card['categoryName']
            image = imagePrefix + card['image']

            for variant in card['variants']:
                if variant['quantity'] <= 0:
                    continue

                price = variant['price']
                condition = variant['name']


                if condition == "Lightly Played":
                    condition = "LP"
                elif condition == "NM/Mint":
                    condition = "NM"
                elif condition == "Moderately Played":
                    condition = "MP"
                elif condition == "Sleeve Playable":
                    condition = "HP"
                # no DMG condition from what I can tell
                # we want the link to look like this
                # "{self.siteUrl}/store/category/{categoryName}/item/{inventoryID}/{inventoryName}"
                # We also need to replace spaces with '_' in each of the variables
                

                # construct link to card
                categoryName = card['categoryName'].replace(' ', '%20')
                inventoryID = str(card['inventoryID'])
                inventoryName = card['inventoryName'].replace(' ', '_')


                



                link = f"{self.siteUrl}/store/category/{categoryName}/item/{inventoryID}/{inventoryName}"
                self.results.append({
                    'name': name,
                    'set': setName,
                    'foil': foil,
                    'condition': condition,
                    'price': price,
                    'image': image,
                    'link': link,
                    'website': self.website
                })