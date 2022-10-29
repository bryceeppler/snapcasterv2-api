from bs4 import BeautifulSoup
import requests
from .Scraper import Scraper

class ACGamesScraper(Scraper):
    """
    ACGames uses no api, everything is server side.
    So we need to use bs4 to scrape the data.

    Split cards can be searched using one or two slashes in the url, the results are the same.
    We just have to convert slashes to "%2F" in the url.

    commas: %2C
    apostrophes: %27
    spaces: +
    slashes: %2F
    dashes: included in the name, don't touch
    """
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.baseUrl = 'https://acgamesonline.crystalcommerce.com/'
        self.website = 'acgames'
        self.url = self.createUrl()

    def createUrl(self):

        urlCardName = self.cardName.replace(',', '%2C').replace("'", '%27').replace(' ', '+').replace('/', '%2F')
        # we need '/products/search?page=${ pageNumber }&q=' to search for the card and iterate through the pages
        searchPrepend = '/products/search?page=${ pageNumber }&q=' 
        return self.baseUrl + searchPrepend + urlCardName

    def scrape(self):
        page = requests.get(self.url)
    
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('li', class_='product')

        if len(results) == 0:
            return None
        
        for result in results:
            name = result.select_one('div.meta h4.name').getText()
            if "Art Card" in name:
                continue
            # foil status is in the name as - Foil, same with Borderless
            foil = False
            borderless = False
            if ' - Foil' in name:
                foil = True
                name = name.replace(' - Foil', '')
            if ' - Borderless' in name:
                borderless = True
                name = name.replace(' - Borderless', '')

            if ' - ' in name:
                # split card
                name = name.split(' - ')[0]

            if self.cardName.lower() not in name.lower():
                continue


            # get the href from the a tag with an itemprop="url" attribute
            link = self.baseUrl + result.select_one('a[itemprop="url"]')['href']
            if 'magic_singles' not in link:
                # not a magic card
                continue

            # get the set from div.meta span.category
            setName = result.select_one('div.meta span.category').getText()

            # remove any other tags we dont want
            if ' - ' in setName:
                setName = setName.split(' - ')[0]

            # get the image src from inside from the div with image class
            image = result.select_one('div.image img')['src']

            # need to do this for each variant
            for variant in result.select('div.variants div.variant-row'):
                condition = variant.select_one('span.variant-short-info').getText()
                if "Out of stock" in condition:
                    continue
                if 'NM' in condition:
                    condition = 'NM'
                elif 'LP' in condition:
                    condition = 'LP'
                elif 'MP' in condition:
                    condition = 'MP'
                elif 'HP' in condition:
                    condition = 'HP'
                elif "DMG" in condition:
                    condition = 'DMG'

                # price comes from the span with class = "regular price"
                price = variant.select_one('span.regular.price').getText().replace('CAD$ ', '')

                card = {
                    'name': name,
                    'set': setName,
                    'condition': condition,
                    'price': price,
                    'link': link,
                    'image': image,
                    'foil': foil,
                    'website': self.website
                }

                self.results.append(card)