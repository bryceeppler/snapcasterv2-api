from bs4 import BeautifulSoup
import requests
from .Scraper import Scraper

class FusionScraper(Scraper):
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.baseUrl = 'https://www.fusiongamingonline.com'
        self.searchUrl = self.baseUrl + "/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D="
        self.url = self.createUrl()
        self.website = 'fusion'

    def createUrl(self):
        url = self.searchUrl
        nameArr = self.cardName.split()
        for word in nameArr:
            url += word
            if word != nameArr[len(nameArr)-1]: # then we don't have last item, add +
                url+= '+' 
        url += '&search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=8&search%5Bwith_descriptor_values%5D%5B6%5D=&search%5Bwith_descriptor_values%5D%5B7%5D=&search%5Bwith_descriptor_values%5D%5B9%5D=&search%5Bwith_descriptor_values%5D%5B10%5D=&search%5Bwith_descriptor_values%5D%5B11%5D=&search%5Bwith_descriptor_values%5D%5B13%5D=&search%5Bwith_descriptor_values%5D%5B348%5D=&search%5Bwith_descriptor_values%5D%5B361%5D=&search%5Bwith_descriptor_values%5D%5B1259%5D=&search%5Bwith_descriptor_values%5D%5B11805%5D=&search%5Bwith_descriptor_values%5D%5B11806%5D=&search%5Bwith_descriptor_values%5D%5B11832%5D=&search%5Bwith_descriptor_values%5D%5B11833%5D=&search%5Bvariants_with_identifier%5D%5B14%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B15%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D='
        return url

    def scrape(self):
        page = requests.get(self.url)
 
        sp = BeautifulSoup(page.text, 'html.parser')
        cards = sp.select('li.product div.inner')
        stockList = []

        for card in cards:
            # Check to see it is a magic card
            # ^^ The link we are using includes this filter

            # Verify card name is correct
            try:
                checkName = card.select_one('div.image-meta div.image a')['title']
            except:
                continue
            if not self.compareCardNames(self.cardName, checkName):
                continue

            # Each condition has it's own product entry on fusion
            # So just get the info for this condition of card



            name = checkName
            link = self.baseUrl + card.select_one('div.image-meta div.image a')['href']
            imageUrl = card.select_one('div.image-meta div.image a img')['src']
            setName = card.select_one('div.image-meta div.meta span.category').getText()

            condition = card.select_one('span.variant-description').getText()
            if "NM" in condition:
                condition="NM"
            elif "Light" in condition:
                condition="LP"
            elif "Moderate" in condition:
                condition="MP"
            elif "Heavy" in condition:
                condition="HP"
            elif "Damaged" in condition:
                condition="HP"

            price = float(card.select_one('form.add-to-cart-form')['data-price'].replace('CAD$ ', ''))
            added = False

            # Check to see if entry already exists in stockList
            try:
                for dict in stockList:
                    if dict['name'].strip() == name.strip() and dict['set'] == setName:
                        # Entry exists, add condition and price to the entry
                        dict['stock'].append({"condition": condition, "price": price})
                        added = True
                        break
            except:
                pass

            # If not, add to stockList
            if not added:
                results = {
                    'name': name,
                    'link': link,
                    'image': imageUrl,
                    'set': setName,
                    'stock': [{"condition": condition, "price": price}],
                    'website': self.website
                }

            stockList.append(results)
  
        self.results = stockList
