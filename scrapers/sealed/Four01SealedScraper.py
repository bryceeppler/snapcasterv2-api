import requests
import json
from .SealedScraper import SealedScraper

# This is scraped using an API requests that returns the stock in json
# is nice

class Four01SealedScraper(SealedScraper):
    """
    Split cards can be searched using "//" as a split

    """
    def __init__(self, setName):
        SealedScraper.__init__(self, setName)
        self.siteUrl = 'https://store.401games.ca'
        self.baseUrl = 'https://ultimate-dot-acp-magento.appspot.com/categories_navigation?request_source=v-next&src=v-next&UUID=d3cae9c0-9d9b-4fe3-ad81-873270df14b5&uuid=d3cae9c0-9d9b-4fe3-ad81-873270df14b5&store_id=17041809&cdn_cache_key=1667566844&api_type=json&category_id=448682319&narrow=[["In+Stock","True"],["Product+Type","Product+Type_Booster+Cases"],["Product+Type","Product+Type_Booster+Boxes"],["Product+Type","Product+Type_Booster+Packs"],["Product+Type","Product+Type_Bundles+&+Fat+Packs"],["Product+Type","Product+Type_Prerelease+Packs"],["Category","Magic:+The+Gathering"]]&facets_required=1&products_per_page=20&page_num=1&with_product_attributes=true&search_within_search='
        self.url = self.createUrl()
        self.website = 'four01'
# https://ultimate-dot-acp-magento.appspot.com/categories_navigation?request_source=v-next&src=v-next&UUID=d3cae9c0-9d9b-4fe3-ad81-873270df14b5&uuid=d3cae9c0-9d9b-4fe3-ad81-873270df14b5&store_id=17041809&cdn_cache_key=1667566844&api_type=json&category_id=448682319&narrow=[["In+Stock","True"],["Product+Type","Product+Type_Booster+Cases"],["Product+Type","Product+Type_Booster+Boxes"],["Product+Type","Product+Type_Booster+Packs"],["Product+Type","Product+Type_Bundles+&+Fat+Packs"],["Product+Type","Product+Type_Prerelease+Packs"],["Category","Magic:+The+Gathering"]]&facets_required=1&products_per_page=20&page_num=1&with_product_attributes=true&search_within_search=
# commander+legends:+battle+for+baldur's+gate
    def createUrl(self):
        url = self.baseUrl
        url += self.setName.replace(" ", "+") 
        return url

    def scrape(self):
        # make the api request
        responseJson = requests.get(self.url)
        # parse the json response
        data = json.loads(responseJson.content) 

        # create a list to return
        cardList = []

        # get the products
        for item in data['items']:
            name = item['l']
            if "commander deck" in name.lower():
                continue
            
            image = item['t']
            link = self.siteUrl + item['u']

            # no stock unless we visit the page
            stock = -1

            tags = self.setTags(name)
            language = self.setLanguage(name)

            for stockItem in item['vra']:
                item = stockItem[1]

                for key in item:
                    if "Sellable" in key:
                        if key[1] == False:
                            continue
                    elif "Price" in key:
                        price = key[1][0].replace("CAD:","")
                
                try:
                    self.results.append({
                        'name': name,
                        'link': link,
                        'image': image,
                        'price': float(price),
                        'stock': stock, # stock is -1 to indicate N/A, but is in stock
                        'website': self.website,
                        'language': language,
                        'tags': tags 
                    })
                except:
                    print("Error: " + name)
                    print(item)
                    print("")

