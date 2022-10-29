from bs4 import BeautifulSoup
import requests
from .Scraper import Scraper

class ManaforceScraper(Scraper):
    """
    Manaforce uses no api, everything is server side.
    So we need to use bs4 to scrape the data.

    The advanced search allows us to request in-stock cards only.
    
    Split cards can be searched using one or two slashes in the url, the results are the same.
    """
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.baseUrl = 'https://www.manaforce.ca'
        self.website = 'manaforce'
        self.url = self.createUrl()

    def createUrl(self):
        # baseUrl + /advanced_search?utf8=✓&search%5Bfuzzy_search%5D= + cardName + &search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D=
        urlCardName = self.cardName.replace(',', '%2C').replace("'", '%27').replace(' ', '+').replace('/', '%2F')
        searchPrepend = '/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D=' 
        searchAppend = '&search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D='
        return self.baseUrl + searchPrepend + urlCardName + searchAppend

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
                name = name.split(' - ')[0]

            if self.cardName.lower() not in name.lower():
                continue

            # get the href from the a tag with an itemprop="url" attribute
            link = self.baseUrl + result.select_one('a[itemprop="url"]')['href']
            if 'magic_the_gathering_singles' not in link:
                # not a magic card
                continue

            # get the set from div.meta span.category
            setName = result.select_one('div.meta span.category').getText()

            # remove any other tags we dont want
            if ' - ' in setName:
                setName = setName.split(' - ')[0]

            # get the image src from inside from the div with image class
            image = result.select_one('div.image img')['src']
            for variant in result.select('div.variants div.variant-row'):
                condition = variant.select_one('span.variant-short-info').getText()
                if 'Near Mint' in condition:
                    condition = 'NM'
                elif 'Light' in condition:
                    condition = 'LP'
                elif 'Moderate' in condition:
                    condition = 'MP'
                elif 'Heav' in condition:
                    condition = 'HP'
                elif "dmg" or "dam" in condition.lower():
                    condition = 'DMG'

                # price comes from the span with class = "regular price"
                price = variant.select_one('span.regular.price').getText().replace('CAD$ ', '')

                card = {
                    'name': name,
                    'set': setName,
                    'condition': condition,
                    'price': float(price),
                    'link': link,
                    'image': image,
                    'foil': foil,
                    'website': self.website
                }

                self.results.append(card)