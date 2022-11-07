from bs4 import BeautifulSoup
import requests
from .SealedScraper import SealedScraper

class ConnectionGamesSealedScraper(SealedScraper):
    """
    Connection games uses no api, everything is server side.
    So we need to use bs4 to scrape the data.

    The advanced search allows us to request in-stock cards only.

    commas: %2C
    apostrophes: %27
    spaces: +
    slashes: %2F
    dashes: included in the name, don't touch

    """
    def __init__(self, setName):
        SealedScraper.__init__(self, setName)
        self.baseUrl = 'https://www.theconnectiongames.com'
        self.website = 'connectiongames'
        self.url = self.createUrl()

    def createUrl(self):
        return ""
        # urlsetName = self.setName.replace(',', '%2C').replace("'", '%27').replace(' ', '+').replace('/', '%2F')
        # searchPrepend = '/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D=' 
        # searchAppend = '&search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D='
        # return self.baseUrl + searchPrepend + urlsetName + searchAppend

    def scrape(self):
        page = requests.get(self.url)
    
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('li', class_='product')

        if len(results) == 0:
            return None
        
        for result in results:
            name = result.select_one('div.meta h4.name').getText()
            # get the href from the a tag with an itemprop="url" attribute
            link = self.baseUrl + result.select_one('a[itemprop="url"]')['href']
            if 'magic_singles' not in link:
                # not a magic card
                continue

            # get the set from div.meta span.category
            setName = result.select_one('div.meta span.category').getText()

            # get the image src from inside from the div with image class
            image = result.select_one('div.image img')['src']

            for variant in result.select('div.variants div.variant-row'):
                condition = variant.select_one('span.variant-short-info').getText()
                # price comes from the span with class = "regular price"
                price = variant.select_one('span.regular.price').getText().replace('CAD$ ', '')

