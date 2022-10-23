from bs4 import BeautifulSoup
import requests
from .Scraper import Scraper


class GauntletScraper(Scraper):
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.baseUrl = 'https://www.gauntletgamesvictoria.ca'
        self.searchUrl = self.baseUrl + '/products/search?q='
        self.url = self.createUrl()
        self.website = 'gauntlet'

    def createUrl(self):
        url = self.searchUrl
        nameArr = self.cardName.split()
        for word in nameArr:
            url += word
            if word != nameArr[len(nameArr)-1]: # then we don't have last item, add +
                url+= '+' 
            else: url+= '&c1'
        return url

    def scrape(self):
        page = requests.get(self.url)
 
        sp = BeautifulSoup(page.text, 'html.parser')
        cards = sp.select('li.product div.inner')

        for card in cards:
            # Check to see it is a magic card
            # we will do this by checking the link to the product. if it contains 
            # "magic_singles" then it is a magic card
            link = self.baseUrl + card.select_one('div.image a')['href']
            if "magic_singles" not in link:
                continue

            # Verify card name is correct
            checkName = card.select_one('div.image a')['title']
            if not self.compareCardNames(self.cardName, checkName):
                continue


            name = card.select_one('div.image a')['title']
            imageUrl = card.select_one('img')['src']
            setName = card.select_one('span.category').getText()

            # Sometimes the foil status is in the name, so we need to remove it
            # Card Name - Foil
            foil = False
            if '- Foil' in name:
                name = name.replace('- Foil', '').rstrip()
                foil = True

            # sometimes there are other tags like "Card Name - Borderless"
            # remove em
            if '-' in name:
                name = name.split('-')[0].rstrip()
            
            # For this card variant, get the stock
            # variantStockList = []
            variantConditions = card.select('div.variant-row')

            # For each item, get the condition and price
            for c in variantConditions:
                if 'no-stock' in c['class']:
                    continue
                condition = c.select_one('span.variant-description').getText()
            
                if "NM" or "Brand New" in condition:
                    condition="NM"
                elif "Light" in condition:
                    condition="LP"
                elif "Moderate" in condition:
                    condition="MP"
                elif "Heavy" in condition:
                    condition="HP"
                elif "Damaged" in condition:
                    condition="HP"

                price = float(c.select_one('form.add-to-cart-form')['data-price'].replace('CAD$ ', ''))

                # Verify condition and price are not duplicates
                print("condition, price: ", condition, price)
                cardObj = {
                    "name": name,
                    "image": imageUrl,
                    "link": link,
                    "set": setName,
                    "foil": foil,
                    "condition": condition,
                    "price": price,
                    "website": self.website
                }
                # check if identicle cardObj is in self.results
                if cardObj not in self.results:
                    self.results.append(cardObj)
