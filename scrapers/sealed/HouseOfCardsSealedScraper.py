from bs4 import BeautifulSoup
import requests
from .SealedScraper import SealedScraper
# from SealedScraper import SealedScraper
import sys
import json


class HouseOfCardsSealedScraper(SealedScraper):
    """
    This is a bit different, The sealed portion of the ecommerce site it rendered
    serverside, so the API isn't exposed. I will have to check three different pages:

    1. https://houseofcards.ca/collections/booster-boxes?page=2
    2. https://houseofcards.ca/collections/booster-packs?page=2
    3. https://houseofcards.ca/collections/bundles?page=1

    Also, there is no way to reliably search for a specific set, so I will have to
    iterate through all the sets and check if the name matches. This is a bit slow,
    so I will post the results to a database on a cron job and then query that?

    So Step 1 is to return the info from the database, and step 2 is to update the
    database.
    """

    def __init__(self, setName):
        SealedScraper.__init__(self, setName)
        self.baseUrl = 'https://houseofcards.ca'
        self.website='houseOfCards'

    def getResults(self):
        # we are overriding this for now. HouseofCards scrapes ALL sealed data, so we will filter out
        # excess stuff here. But ideally we don't scrape it all every time. Push to database instead...
        self.results = [result for result in self.results if self.setName.lower() in result['name'].lower()]
        return self.results

    def scrape(self):
        # We need to check three different pages and they are all paginated
        curPage = 1
        boosterPackUrl = self.baseUrl + '/collections/booster-packs?page=' + str(curPage)
        boosterBoxUrl = self.baseUrl + '/collections/booster-boxes?page=' + str(curPage)
        bundleUrl = self.baseUrl + '/collections/bundles?page=' + str(curPage)

        for url in [boosterPackUrl, boosterBoxUrl, bundleUrl]:
            while True:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                products = soup.find_all('div', class_='productCard__card')

                for product in products:
                    try:
                        name = product.find('p', class_='productCard__title').find('a').text
                        price = product.find('p', class_='productCard__price').text.strip()
                        tags = self.setTags(name)
                        image = "https:" + product.find('img', class_='productCard__img')['data-src']
                        print("image: ", image)
                        # if there is a newline, take the first line
                        if '\n' in price:
                            price = price.split('\n')[0] 
                        price = float(price.replace('$', '').replace(' CAD', '').replace(',',"").strip())
                        self.results.append({
                            'name': name,
                            'link': self.baseUrl + product.find('a', class_='productCard__a')['href'],
                            'image': image,
                            'price': price,
                            'stock': -1,
                            'website': self.website,
                            'language': 'English',
                            'tags': tags
                        }) 

                    except Exception as e:
                        print(e)
                        # print error details
                        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                        print("Error parsing product")

                # Check the ol.pagination and see if there is an li element with a class of disabled that contains the text 'Next'
                pagination = soup.find('ol', class_='pagination')
                if (pagination):
                    buttons = pagination.find_all('li', class_='disabled')
                    # If there is a disabled button with "next" in it, we are done, exit the while loop
                    if any('Next' in button.text for button in buttons):
                        curPage = 1
                        break
                                    
                    elif curPage > 10:
                        # just incase we get stuck in an infinite loop
                        curPage = 1
                        break

                    else:
                        curPage += 1
                        url = url[:-1] + str(curPage)
                else:
                    curPage = 1
                    break
        

def main():
    scraper = HouseOfCardsSealedScraper('Dominaria')
    scraper.scrape()

if __name__ == "__main__":
    main()