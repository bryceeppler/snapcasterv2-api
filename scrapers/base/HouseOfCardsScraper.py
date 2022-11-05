from bs4 import BeautifulSoup
import requests
from .Scraper import Scraper


class HouseOfCardsScraper(Scraper):
    """
    We can actually refactor this to use their API, it's exposed on the advanced search
    for MTG singles.
    
    Split cards can be searched using "//" as a split
    """
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.baseUrl = 'https://houseofcards.ca'
        self.searchUrl = self.baseUrl + '/search?page=1&q=%2A'
        self.url = self.createUrl()
        self.website='houseOfCards'

    def createUrl(self):
        url = self.searchUrl
        nameArr = self.cardName.split()
        for word in nameArr:
            url += word
            if word != nameArr[len(nameArr)-1]: # then we don't have last item, add %20
                url+= '%20' 
            else: url+= '%2A'
        return url

    def scrape(self):
        page = requests.get(self.url)

        sp = BeautifulSoup(page.text, 'html.parser')
        cards = sp.select('div.productCard__card')

        stockList = []

        for card in cards:
            # Product tiles are split into upper and lower divs
            productCardLower = card.select_one('div.productCard__lower')
            productCardUpper = card.select_one('div.productCard__upper')

            # check to see its a magic card
            if card['data-producttype'] != 'MTG Single':
                continue

            # check to see name is correct
            checkName = productCardLower.select_one('a').getText()
            if "art card" in checkName.lower():
                continue
            if not self.compareCardNames(self.cardName, checkName):
                continue


            # <a> tag has href pointing to card's page and inner text is the card's name
            tag = productCardLower.select_one('a')
            name = tag.getText()
            # sometimes there are weird tags in the name like "Card name (Borderless)"
            # remove them
            if '(' in name:
                name = name.split('(')[0]
            name = name.strip()
                
            baseUrl = 'https://houseofcards.ca'
            link =  baseUrl + tag.get('href')

            # image
            imageUrl = productCardUpper.select_one('img').attrs['data-src']
            imageUrl = imageUrl.replace('//', 'https://')

            # set name
            setName = productCardLower.select_one('p.productCard__setName').getText()

            # sometimes the set name has "Extended" at the end, remove it
            if 'Extended' in setName:
                setName = setName.split('Extended')[0].strip()


            # For this card variant, get the stock
            variantStockList = []
            variantConditions = productCardLower.select('li.productChip')
            for c in variantConditions:
                if c['data-variantavailable'] == 'true':
                    foil = False
                    if ('Foil' in c['data-varianttitle']):
                        foil = True

                    condition = c.getText().strip()
                    price = float(c['data-variantprice']) / 100
                    variantStockList.append({"condition": condition, "price": price})
                    self.results.append({
                        "name": name,
                        "image": imageUrl,
                        "link": link,
                        "set": setName,
                        "condition": condition,
                        "price": price,
                        "website": self.website,
                        "foil": foil
                    })

