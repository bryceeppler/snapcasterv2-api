from bs4 import BeautifulSoup
import requests
from .Scraper import Scraper


class KanatacgScraper(Scraper):
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.baseUrl = 'https://www.kanatacg.com'
        self.searchUrl = self.baseUrl + '/products/search?query='
        self.url = self.createUrl()
        self.website='kanatacg'

    def createUrl(self):
        url = self.searchUrl
        nameArr = self.cardName.split()
        for word in nameArr:
            url +=word
            if word != nameArr[len(nameArr)-1]: # then we don't have last item, add +
                url+= '+'
            else: pass
        return url

    def scrape(self):
        page = requests.get(self.url)

        sp = BeautifulSoup(page.text, 'html.parser')
        cards = sp.select('table.invisible-table tr')

        stockList = []

        for card in cards:
            # Check to see it is a magic card
            # TODO

            # Verify card name is correct
            checkNameTag = card.select('td')[1]
            checkName = checkNameTag.select_one('a')        
            if not checkName:
                continue
            if not self.compareCardNames(self.cardName, checkName.getText()):
                continue

            # For this card variant, get the stock
            variantStockList = []
            variantConditions = card.select('tr.variantRow')

            # For each item get the condition and price
            for c in variantConditions:
                condition = c.select_one('td.variantInfo').getText().replace('Condition: ', '').replace('-Mint, English', '')
                if "Brand New" in condition: # then it's not a MTG single
                    continue
                elif "NM" in condition:
                    condition="NM"
                elif "Slight" in condition:
                    condition="LP"
                elif "Moderate" in condition:
                    condition="MP"
                elif "Heav" in condition:
                    condition="HP"
                elif "Damaged" or "DMG" in condition:
                    condition="HP"
                price = float(c.select('td')[1].getText().replace('CAD$ ', ''))
                if (condition, price) not in variantStockList:
                    variantStockList.append({"condition": condition, "price": price})
                
            # If stockList is empty, continue
            if not variantStockList:
                continue

            name = card.select('td')[1].select_one('a').getText()
            link = self.baseUrl + card.select('td')[1].select_one('a')['href']
            imageUrl = card.select_one('td a')['href']
            setName = card.select('td')[1].select_one('small').getText()

            results = {
                'name': name,
                'link': link,
                'image': imageUrl,
                'set': setName,
                'stock': variantStockList,
                'website': self.website
            }
            stockList.append(results)

        self.results = stockList