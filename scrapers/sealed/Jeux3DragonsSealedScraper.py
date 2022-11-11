from bs4 import BeautifulSoup
import requests
from .SealedScraper import SealedScraper


class Jeux3DragonsSealedScraper(SealedScraper):
    """
    Jeux3Dragons can be scraped by creating a URL from their advanced search
    This allows us to search for in stock sets


    Spaces are replaced with "+"
    Slashes - %2F
    Commas - %2C
    Apostrophes - %27
    """

    def __init__(self, setName):
        SealedScraper.__init__(self, setName)
        self.baseUrl = 'https://www.jeux3dragons.com'
        self.url = self.createUrl()
        self.website = 'jeux3dragons'

    def createUrl(self):
        # https://www.jeux3dragons.com/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D=
        # dominaria
        # &search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=6374&search%5Bcategory_ids_with_descendants%5D%5B%5D=6382&search%5Bwith_descriptor_values%5D%5B4116%5D%5B%5D=Booster+Boxes&search%5Bwith_descriptor_values%5D%5B4116%5D%5B%5D=Bundles&search%5Bwith_descriptor_values%5D%5B4116%5D%5B%5D=Booster+Packs&search%5Bwith_descriptor_values%5D%5B4116%5D%5B%5D=Pre-release+Kits&search%5Bvariants_with_identifier%5D%5B19%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B4420%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D=
        # make set name url friendly
        # Spaces are replaced with "+"
        # Slashes - %2F
        # Commas - %2C
        # Apostrophes - %27
        urlsetName = self.setName.replace(
            ' ', '+').replace('/', '%2F').replace(',', '%2C').replace("'", '%27').replace(':', '%3A')
        prefix = self.baseUrl + '/advanced_search?utf8=%E2%9C%93&search%5Bfuzzy_search%5D='
        suffix = '&search%5Btags_name_eq%5D=&search%5Bsell_price_gte%5D=&search%5Bsell_price_lte%5D=&search%5Bbuy_price_gte%5D=&search%5Bbuy_price_lte%5D=&search%5Bin_stock%5D=0&search%5Bin_stock%5D=1&buylist_mode=0&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=&search%5Bcategory_ids_with_descendants%5D%5B%5D=6374&search%5Bcategory_ids_with_descendants%5D%5B%5D=6382&search%5Bwith_descriptor_values%5D%5B4116%5D%5B%5D=Booster+Boxes&search%5Bwith_descriptor_values%5D%5B4116%5D%5B%5D=Bundles&search%5Bwith_descriptor_values%5D%5B4116%5D%5B%5D=Booster+Packs&search%5Bwith_descriptor_values%5D%5B4116%5D%5B%5D=Pre-release+Kits&search%5Bvariants_with_identifier%5D%5B19%5D%5B%5D=&search%5Bvariants_with_identifier%5D%5B4420%5D%5B%5D=&search%5Bsort%5D=name&search%5Bdirection%5D=ascend&commit=Search&search%5Bcatalog_group_id_eq%5D='
        return prefix + urlsetName + suffix

    def scrape(self):
        page = requests.get(self.url)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('li', class_='product')

        if len(results) == 0:
            return None

        for result in results:
            name = result.select_one('div.meta h4.name').getText()

            # get the href from the a tag with an itemprop="url" attribute
            link = self.baseUrl + \
                result.select_one('a[itemprop="url"]')['href']

            # get the image src from inside from the div with image class
            image = result.select_one('div.image img')['src']

            language = self.setLanguage(name)
            tags = self.setTags(name)

            for variant in result.select('div.variants div.variant-row'):
                # price comes from the span with class = "regular price"
                price = variant.select_one(
                    'span.regular.price').getText().replace('CAD$ ', '')
                
                stock = variant.select_one('span.variant-qty').getText().replace(' In Stock', '').strip()

                product = {
                    'name': name,
                    'link': link,
                    'image': image,
                    'price': float(price),
                    'stock': int(stock),
                    'website': self.website,
                    'language': language,
                    'tags': tags
                }

                self.results.append(product)
