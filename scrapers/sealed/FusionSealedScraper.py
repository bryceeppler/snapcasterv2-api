from bs4 import BeautifulSoup
import requests
from .SealedScraper import SealedScraper

class FusionSealedScraper(SealedScraper):
    """
    Using advanced search, we can construct a URL for in stock sealed product
    """
    def __init__(self, setName):
        SealedScraper.__init__(self, setName)
        self.baseUrl = 'https://www.fusiongamingonline.com'
        self.url = self.createUrl()
        self.website = 'fusion'

    def createUrl(self):
        prefix = '/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D='
        suffix = '&search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=100&search%5Bcategory_ids_with_descendants%5D%5B%5D=101&search%5Bcategory_ids_with_descendants%5D%5B%5D=105&search%5Bwith_descriptor_values%5D%5B11213%5D=&search%5Bwith_descriptor_values%5D%5B11223%5D=&search%5Bwith_descriptor_values%5D%5B11233%5D=&search%5Bwith_descriptor_values%5D%5B11243%5D=&search%5Bwith_descriptor_values%5D%5B11253%5D=&search%5Bwith_descriptor_values%5D%5B11263%5D=&search%5Bwith_descriptor_values%5D%5B11273%5D=&search%5Bwith_descriptor_values%5D%5B11283%5D=&search%5Bwith_descriptor_values%5D%5B11293%5D=&search%5Bwith_descriptor_values%5D%5B11303%5D=&search%5Bwith_descriptor_values%5D%5B11313%5D=&search%5Bwith_descriptor_values%5D%5B11323%5D=&search%5Bwith_descriptor_values%5D%5B11333%5D=&search%5Bwith_descriptor_values%5D%5B11343%5D=&search%5Bwith_descriptor_values%5D%5B11353%5D=&search%5Bwith_descriptor_values%5D%5B11363%5D=&search%5Bwith_descriptor_values%5D%5B11373%5D=&search%5Bwith_descriptor_values%5D%5B11383%5D=&search%5Bwith_descriptor_values%5D%5B11393%5D=&search%5Bwith_descriptor_values%5D%5B11403%5D=&search%5Bwith_descriptor_values%5D%5B11413%5D=&search%5Bwith_descriptor_values%5D%5B11423%5D=&search%5Bwith_descriptor_values%5D%5B11433%5D=&search%5Bwith_descriptor_values%5D%5B11443%5D=&search%5Bwith_descriptor_values%5D%5B11453%5D=&search%5Bwith_descriptor_values%5D%5B11463%5D=&search%5Bwith_descriptor_values%5D%5B11473%5D=&search%5Bwith_descriptor_values%5D%5B11483%5D=&search%5Bwith_descriptor_values%5D%5B11493%5D=&search%5Bwith_descriptor_values%5D%5B11503%5D=&search%5Bwith_descriptor_values%5D%5B11923%5D=&search%5Bwith_descriptor_values%5D%5B11924%5D=&search%5Bvariants_with_identifier%5D%5B19%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D='
        urlSetName = self.setName.replace(' ', '+')
        return self.baseUrl + prefix + urlSetName + suffix

    def scrape(self):
        page = requests.get(self.url)

        try:
            sp = BeautifulSoup(page.text, 'html.parser')
            mainSection = sp.select_one("section.main")
            products = mainSection.select('li.product div.inner')

            for product in products:
                name = product.select_one('div.meta h4.name').text
                link = self.baseUrl + product.select_one('div.image-meta div.image a')['href']
                image = product.select_one('div.image-meta div.image a img')['src']
                price = product.select_one('form.add-to-cart-form')['data-price'].replace('CAD$ ', '')
                stock = product.select_one('span.variant-qty').text.replace(" In Stock", "")
                language = self.setLanguage(name)
                name = self.removeLanguage(name).replace(" - ", " ").strip()
                tags = self.setTags(name)

                self.results.append({
                    'name': name,
                    'link': link,
                    'image': image,
                    'price': float(price),
                    'stock': int(stock),
                    'website': self.website,
                    'language': language,
                    'tags': tags,
                })

        except Exception as e:
            print(e)
            print('Error scraping Fusion')
            print(self.url)

  
