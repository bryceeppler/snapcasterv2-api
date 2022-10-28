from bs4 import BeautifulSoup
import requests
from .Scraper import Scraper


class GamezillaScraper(Scraper):
    """
    Split cards can be searched using "//" as a split
    """
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.baseUrl = 'https://gamezilla.ca'
        self.searchUrl = self.baseUrl + '/search?page=1&q='
        self.url = self.createUrl()
        self.website = 'gamezilla'

        # https://gamezilla.ca/search?q=Elspeth%2C+Sun%27s*+product_type%3A%22mtg%22

    def createUrl(self):
        # make cardName url friendly
        # spaces = +
        # / = %2F
        # ' = %27
        # , = %2C
        # " = %22
        urlCardName = self.cardName.replace(' ', '+').replace('/', '%2F').replace("'", "%27").replace(',', '%2C')
        return self.searchUrl + urlCardName + '*+product_type%3A%22mtg%22'
        

    def scrape(self):
        page = requests.get(self.url)
 
        sp = BeautifulSoup(page.text, 'html.parser')
        cards = sp.select('div.col-md-4')

        for card in cards:
            # if sold out, skip
            if "Sold Out" in card.select_one('p.productPrice').text:
                continue

            cardNameAndSet = card.select_one('p.productTitle').getText()

            # cardNameAndSet = "Card Name [Card set]"
            # we need to split the card name and set
            cardName = cardNameAndSet.split(' [')[0].strip()
            cardSet = cardNameAndSet.split(' [')[1].replace(']', '').strip()

            link = self.baseUrl + card.select_one('a.productLink')['href']
            image = "https:" + card.select_one('div.imgWrapper img')['src']

            # Verify card name is correct
            if not self.compareCardNames(self.cardName, cardName):
                continue

            # Iterate over variants in the div class="product Mob" 
            variants = card.select_one('div.product.Mob').select_one('div.buyWrapper').select('div.addNow')
            for variant in variants:
                conditionAndPrice = variant.select_one('p').getText()
                foil = False
                if "Foil" in conditionAndPrice:
                    foil = True
                
                condition = "DMG"
                if "NM" in conditionAndPrice:
                    condition = "NM"
                elif "LP" in conditionAndPrice:
                    condition = "LP"
                elif "MP" in conditionAndPrice:
                    condition = "MP"
                elif "HP" in conditionAndPrice:
                    condition = "HP"

                price = float(conditionAndPrice.split('(')[1].replace("$", "").split(')')[0].strip())

                self.results.append({
                    'name': cardName,
                    'image': image,
                    'link': link,
                    'set': cardSet,
                    'foil': foil,
                    'condition': condition,
                    'price': price,
                    'website': self.website
                })