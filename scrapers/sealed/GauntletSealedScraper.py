from bs4 import BeautifulSoup
import requests
from .SealedScraper import SealedScraper

class GauntletSealedScraper(SealedScraper):
    """
    We can apply the following filters by adding to the link in the advanced search
    - in stock
    - booster boxes
    - booster packs
    - bundles

    https://www.gauntletgamesvictoria.ca/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D=
    dominaria
    &search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=105&search%5Bcategory_ids_with_descendants%5D%5B%5D=101&search%5Bcategory_ids_with_descendants%5D%5B%5D=100&search%5Bwith_descriptor_values%5D%5B17343%5D=&search%5Bwith_descriptor_values%5D%5B17353%5D=&search%5Bwith_descriptor_values%5D%5B17363%5D=&search%5Bwith_descriptor_values%5D%5B17373%5D=&search%5Bwith_descriptor_values%5D%5B17393%5D=&search%5Bwith_descriptor_values%5D%5B17413%5D=&search%5Bwith_descriptor_values%5D%5B17423%5D=&search%5Bwith_descriptor_values%5D%5B17443%5D=&search%5Bwith_descriptor_values%5D%5B17544%5D=&search%5Bwith_descriptor_values%5D%5B17545%5D=&search%5Bvariants_with_identifier%5D%5B19%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D=
    
    https://www.gauntletgamesvictoria.ca/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D=
    Innistrad%3A+midnight+hunt
    &search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=105&search%5Bcategory_ids_with_descendants%5D%5B%5D=101&search%5Bcategory_ids_with_descendants%5D%5B%5D=100&search%5Bwith_descriptor_values%5D%5B17343%5D=&search%5Bwith_descriptor_values%5D%5B17353%5D=&search%5Bwith_descriptor_values%5D%5B17363%5D=&search%5Bwith_descriptor_values%5D%5B17373%5D=&search%5Bwith_descriptor_values%5D%5B17393%5D=&search%5Bwith_descriptor_values%5D%5B17413%5D=&search%5Bwith_descriptor_values%5D%5B17423%5D=&search%5Bwith_descriptor_values%5D%5B17443%5D=&search%5Bwith_descriptor_values%5D%5B17544%5D=&search%5Bwith_descriptor_values%5D%5B17545%5D=&search%5Bvariants_with_identifier%5D%5B19%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D=
    """

    def __init__(self, setName):
        SealedScraper.__init__(self, setName)
        self.website = 'gauntlet'
        urlPrefix = 'https://www.gauntletgamesvictoria.ca/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D='
        urlSuffix = '&search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=105&search%5Bcategory_ids_with_descendants%5D%5B%5D=101&search%5Bcategory_ids_with_descendants%5D%5B%5D=100&search%5Bwith_descriptor_values%5D%5B17343%5D=&search%5Bwith_descriptor_values%5D%5B17353%5D=&search%5Bwith_descriptor_values%5D%5B17363%5D=&search%5Bwith_descriptor_values%5D%5B17373%5D=&search%5Bwith_descriptor_values%5D%5B17393%5D=&search%5Bwith_descriptor_values%5D%5B17413%5D=&search%5Bwith_descriptor_values%5D%5B17423%5D=&search%5Bwith_descriptor_values%5D%5B17443%5D=&search%5Bwith_descriptor_values%5D%5B17544%5D=&search%5Bwith_descriptor_values%5D%5B17545%5D=&search%5Bvariants_with_identifier%5D%5B19%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D='
        # make setName url friendly
        # spaces - +
        # : - %3A
        # , - %2C
        # ' - %27
        # " - %22
        # ( - %28
        # ) - %29
        # / - %2F
        urlSetName = setName.replace(' ', '+').replace(':', '%3A').replace(',', '%2C').replace("'", '%27').replace('"', '%22').replace('(', '%28').replace(')', '%29').replace('/', '%2F')
        self.url = urlPrefix + urlSetName + urlSuffix

    def scrape(self):

        page = requests.get(self.url)
 
        sp = BeautifulSoup(page.text, 'html.parser')
        products = sp.select('li.product div.inner')
        # print("products: ", len(products))
        for product in products:
            link = 'https://www.gauntletgamesvictoria.ca' + product.select_one('div.image a')['href']
            name = product.select_one('div.image a')['title']
            imageUrl = product.select_one('img')['src']
            price = product.select_one('div.variant-row').select_one('form.add-to-cart-form')['data-price'].replace("CAD$ ","")
            stock = product.select_one('div.variant-row span.variant-qty').text.replace(" In Stock", "")
            tags = self.setTags(name)

            self.results.append({
                'name': name,
                'link': link,
                'image': imageUrl,
                'price': float(price),
                'stock': int(stock),
                'website': self.website,
                'language': self.setLanguage(name),
                'tags': tags,
            })