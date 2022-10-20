from bs4 import BeautifulSoup
import requests
import json
from .Scraper import Scraper

# This is scraped using an API requests that returns the stock in json
# is nice

class Four01Scraper(Scraper):
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.siteUrl = 'https://store.401games.ca'
        self.baseUrl = 'https://ultimate-dot-acp-magento.appspot.com/full_text_search?request_source=v-next&src=v-next&UUID=d3cae9c0-9d9b-4fe3-ad81-873270df14b5&uuid=d3cae9c0-9d9b-4fe3-ad81-873270df14b5&store_id=17041809&cdn_cache_key=1661088450&api_type=json&facets_required=1&products_per_page=20&narrow=[[%22In+Stock%22,%22True%22],[%22Category%22,%22Magic:+The+Gathering+Singles%22]]&q='
        self.url = self.createUrl()
        self.website = 'four01'

    def createUrl(self):
        url = self.baseUrl
        nameArr = self.cardName.split()
        for word in nameArr:
            url += word
            if word != nameArr[len(nameArr)-1]: # then we don't have last item, add +
                url+= '+' 
        url += '&page_num=1&sort_by=relevency&with_product_attributes=true'
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
            set = item['v']
            image = item['t']
            url = self.siteUrl + item['u']

            if not self.compareCardNames(self.cardName, name):
                continue 
            
            stock = []
            for stockItem in item['vra']:
                item = stockItem[1]
                if ['Sellable',[False]] in item:
                    continue
                
                if item[0][0] == 'Condition':
                    condition = item[0][1][0]

                    if "NM" in condition:
                        condition="NM"
                    elif "SP" in condition:
                        condition="LP"
                    elif "MP" in condition:
                        condition="MP"
                    elif "HP" in condition:
                        condition="HP" 
                    elif "DMG" in condition:
                        condition="HP"
                    elif "Damaged" in condition:
                        condition="HP"
                    elif "Default" in condition:
                        condition="NM"

                    price = float(item[1][1][0].replace("CAD:" , ""))
                    stock.append({"condition": condition, "price": price})
                
                elif item[0][0] == 'Price':
                    try:
                        condition = item[3][1][0]
                        if "NM" in condition:
                            condition="NM"
                        elif "SP" in condition:
                            condition="LP"
                        elif "MP" in condition:
                            condition="MP"
                        elif "HP" in condition:
                            condition="HP" 
                        elif "DMG" in condition:
                            condition="HP"
                        elif "Damaged" in condition:
                            condition="HP"
                        elif "Default" in condition:
                            condition="NM"

                        price = float(item[0][1][0].replace("CAD:" , ""))
                        stock.append({'condition':condition, 'price':price})
                    except:
                        pass


            cardList.append({
                'name': name,
                'set': set,
                'image': image,
                'link': url,
                'stock': stock,
                'website': self.website
            })

        self.results = cardList


