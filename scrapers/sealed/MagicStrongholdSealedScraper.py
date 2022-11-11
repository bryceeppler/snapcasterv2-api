import requests
import json
from .SealedScraper import SealedScraper
import sys
import os
import psycopg2
import dotenv
dotenv.load_dotenv()


class MagicStrongholdSealedScraper(SealedScraper):
    """
    We can get stock for Magic Stronghold by hitting their API.
    We have to hit the API for each product category 
    - booster box, booster pack, bundles and prerelase kits.

    Since this is only going to be 4 requests, we will only refresh stock if it has not been
    refreshed in the last 30 minutes.
    """

    def __init__(self, setName):
        SealedScraper.__init__(self, setName)
        self.siteUrl = 'https://www.magicstronghold.com'
        self.apiUrl = "https://api.conductcommerce.com/v1/getProductListings"
        self.website = 'magicstronghold'

    def getResults(self):
        # We are overriding this so we can filter out results that don't match the set name
        self.results = [result for result in self.results if self.setName.lower() in result['name'].lower()]
        return self.results

    def scrape(self):
        # We want to check the database for houseofcards data, if it has been updated in the last 8 hours, return the data
        # otherwise, scrape the site and update the database, then return the data

        try:
            # connect to the database
            conn = psycopg2.connect(
                dbname=os.environ['PG_DB'],
                user=os.environ['PG_USER'],
                password=os.environ['PG_PASSWORD'],
                host=os.environ['PG_HOST'],
                port=os.environ['PG_PORT']
            )
            cur = conn.cursor()

            try:
                # check if the data has been updated in the last 30 mins
                cur.execute(
                    "SELECT * FROM sealed_prices WHERE website = 'magicstronghold' AND updated_at > NOW() - INTERVAL '30 minutes'")
                rows = cur.fetchall()
            except:
                print("Error selecting from database")
                conn.rollback()
                rows = []

            # if there is data, return it
            if len(rows) > 0:
                # close db connection, we don't need it anymore
                cur.close()
                conn.close()
                # return the data
                self.results = [{
                    'name': row[1],
                    'link': row[2],
                    'image': row[3],
                    'price': row[4],
                    'stock': row[5],
                    'website': row[6],
                    'language': row[7],
                    'tags': row[8],
                } for row in rows]
                return self.results

            # otherwise, scrape the site and update the database
            else:
                # First hit the 4 API endpoints to get the data, then update the database

                # BOOSTER BOXES
                boosterBoxResponse = requests.post(self.apiUrl, json={
                    "category": "Booster Boxes",
                    "host": "www.magicstronghold.com",
                })
                boosterBoxData = json.loads(boosterBoxResponse.text)

                # BOOSTER PACKS
                boosterPackResponse = requests.post(self.apiUrl, json={
                    "category": "Booster Packs",
                    "host": "www.magicstronghold.com",
                })
                boosterPackData = json.loads(boosterPackResponse.text)

                # BUNDLES
                bundleResponse = requests.post(self.apiUrl, json={
                    "category": "Fat Packs & Bundles",
                    "host": "www.magicstronghold.com",
                })
                bundleData = json.loads(bundleResponse.text)

                # PRERELEASE KITS
                prereleaseKitResponse = requests.post(self.apiUrl, json={
                    "category": "Pre-Release & Promo Packs",
                    "host": "www.magicstronghold.com",
                })
                prereleaseKitData = json.loads(prereleaseKitResponse.text)

                # join data[result][listings] from each data object into one array
                allData = boosterBoxData['result']['listings'] + boosterPackData['result']['listings'] + \
                    bundleData['result']['listings'] + \
                    prereleaseKitData['result']['listings']

                # print("Num results: ", len(data['result']['listings']))
                for product in allData:
                    name = product['inventoryName']
                    language = self.setLanguage(name)
                    # replace ()[] with nothing without chaining replace
                    name = self.removeLanguage(name).replace("(", "").replace(
                        ")", "").replace("[", "").replace("]", "").strip()
                    tags = self.setTags(name)
                    if product['image'] is not None:
                        if 'magicstronghold-images.s3.amazonaws.com' in product['image']:
                            image = product['image']
                        else:
                            image = 'https://conduct-catalog-images.s3-us-west-2.amazonaws.com/small/' + \
                                product['image']
                    else:
                        image = ''

                    for variant in product['variants']:
                        quantity = variant['quantity']
                        if quantity < 1:
                            continue
                        price = variant['price']
                        # print name, quantity, price in a nice table
                        # print("{0: <50} {1: <10} {2: <10}".format(name, quantity, price))
                        self.results.append({
                            "name": name,
                            "link": self.siteUrl,
                            "image": image,
                            "price": float(price),
                            "stock": int(quantity),
                            "website": self.website,
                            "language": language,
                            "tags": tags
                        })
                
                # update the database
                # create the table if it doesn't exist, primary key is a composite of name, website, language, and tags
                cur.execute("CREATE TABLE IF NOT EXISTS sealed_prices (id serial, name text, link text, image text, price float, stock int, website text, language text, tags text[], updated_at timestamp DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (name, website, language, tags))")
                # insert the data, if there is a conflict, update the price, link, image, and updated_at
                for result in self.results:
                    cur.execute("INSERT INTO sealed_prices (name, link, image, price, stock, website, language, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (name, website, language, tags) DO UPDATE SET price = EXCLUDED.price, link = EXCLUDED.link, image = EXCLUDED.image, updated_at = EXCLUDED.updated_at", (result['name'], result['link'], result['image'], result['price'], result['stock'], result['website'], result['language'], result['tags']))
                conn.commit()
                # close db connection
                cur.close()
                conn.close()

                # filter self.results to only include the set we are looking for
                self.results = [result for result in self.results if self.setName.lower() in result['name'].lower()]


        except Exception as e:
            print("Error on line {}".format(
                sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

