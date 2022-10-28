from bs4 import BeautifulSoup
import requests
import json
from .Scraper import Scraper

class ExorGamesScraper(Scraper):
    """
    Exor games uses a completely exposed API to get the stock of cards
    We can literally hit the API and get all the information we need

    Split cards can be searched using "//" as a split

    """
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.siteUrl = 'https://www.exorgames.com'
        self.url = "https://portal.binderpos.com/external/shopify/products/forStore"
        self.website = 'exorgames'

    def scrape(self):
        # get the json data from this curl request
# curl 'https://portal.binderpos.com/external/shopify/products/forStore' \
#   -H 'authority: portal.binderpos.com' \
#   -H 'accept: application/json, text/javascript, */*; q=0.01' \
#   -H 'accept-language: en-US,en;q=0.9' \
#   -H 'cache-control: no-cache' \
#   -H 'content-type: application/json; charset=UTF-8' \
#   -H 'origin: https://exorgames.com' \
#   -H 'pragma: no-cache' \
#   -H 'referer: https://exorgames.com/' \
#   -H 'sec-ch-ua: "Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: cross-site' \
#   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' \
#   --data-raw '{"storeUrl":"most-wanted-ca.myshopify.com","game":"mtg","strict":null,"sortTypes":[{"type":"price","asc":false,"order":1}],"variants":null,"title":"Fblthp","priceGreaterThan":0,"priceLessThan":null,"instockOnly":true,"limit":18,"offset":0}' \
#   --compressed
        
        # make the card name url friendly
        cardName = self.cardName.replace('"', '%22')
        
        response = requests.post(self.url, 
            json={
                "storeUrl": "most-wanted-ca.myshopify.com",
                "game": "mtg",
                "strict": None,
                "sortTypes": [
                    {
                        "type": "price",
                        "asc": False,
                        "order": 1
                    }
                ],
                "variants": None,
                "title": cardName,
                "priceGreaterThan": 0,
                "priceLessThan": None,
                "instockOnly": True,
                "limit": 18,
                "offset": 0
            },
            headers={
                "authority": "portal.binderpos.com",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "content-type": "application/json; charset=UTF-8",
                "origin": "https://exorgames.com",
                "pragma": "no-cache",
                "referer": "https://exorgames.com/",
                "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            }
        )
        # Load the response
        data = json.loads(response.text)

        # print (data)
        # parse the json data
        for card in data['products']:
            titleAndSet = card['title']
            # split the title and set
            title = titleAndSet.split("[")[0].strip()
            setName = titleAndSet.split("[")[1].split("]")[0].strip()

            # remove any excess tags inside () or [] in the title
            title = title.split("(")[0].strip()

            image = card['img']
            handle = card['handle']
            link = f"{self.siteUrl}/products/{handle}"

            for variant in card['variants']:
                # this string contains the condition and foil status
                # variant['title'] = "Lightly Played Foil"
                # print the variant as json
                if(variant['quantity'] <= 0):
                    continue

                condition = variant['title'].split(" ")[0].strip()
                # getting the first element here will yield
                # "Lightly" or "Near" or "Moderately" or "Heavily" or "Damaged"
                # We want to code this to "LP" or "NM" or "MP" or "HP" or "DMG"
                if condition == "Lightly":
                    condition = "LP"
                elif condition == "Near":
                    condition = "NM"
                elif condition == "Moderately":
                    condition = "MP"
                elif condition == "Heavily":
                    condition = "HP"
                elif condition == "Damaged":
                    condition = "DMG"
                
                # check if the card is foil
                foil = False
                if "Foil" in variant['title']:
                    foil = True

                price = variant['price']

                self.results.append({
                    'name': title,
                    'link': link,
                    'image': image,
                    'set': setName,
                    'condition': condition,
                    'foil': foil,
                    'price': price,
                    'website': self.website
                })

