from re import I
from unittest import result
from bs4 import BeautifulSoup
import requests
import json
from .Scraper import Scraper

class FaceToFaceScraper(Scraper):
    """
    Everything games uses a completely exposed API to get the stock of cards
    We can literally hit the API and get all the information we need

    https://essearchapi-na.hawksearch.com/api/v2/search
    """
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.siteUrl = 'https://www.facetofacegames.com/'
        self.url = "https://essearchapi-na.hawksearch.com/api/v2/search"
        self.website = 'facetoface'

    def scrape(self):
    # curl 'https://essearchapi-na.hawksearch.com/api/v2/search' \
    #   -H 'authority: essearchapi-na.hawksearch.com' \
    #   -H 'accept: application/json, text/plain, */*' \
    #   -H 'accept-language: en-US,en;q=0.9' \
    #   -H 'cache-control: no-cache' \
    #   -H 'content-type: application/json;charset=UTF-8' \
    #   -H 'origin: https://www.facetofacegames.com' \
    #   -H 'pragma: no-cache' \
    #   -H 'referer: https://www.facetofacegames.com/' \
    #   -H 'sec-ch-ua: "Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"' \
    #   -H 'sec-ch-ua-mobile: ?0' \
    #   -H 'sec-ch-ua-platform: "macOS"' \
    #   -H 'sec-fetch-dest: empty' \
    #   -H 'sec-fetch-mode: cors' \
    #   -H 'sec-fetch-site: cross-site' \
    #   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36' \
    #   --data-raw '{"Keyword":"","FacetSelections":{"tab":["Magic"]},"PageNo":1,"ClientGuid":"30c874915d164f71bf6f84f594bf623f","IndexName":"","ClientData":{"VisitorId":""},"query":"(card\\ name.text: \"Ajani\" OR card\\ name\\ 2.text: \"Ajani\")"}' \
    #   --compressed
        
        print("making the request")
        response = requests.post(self.url, 
            json={
                "Keyword":"",
                "FacetSelections": {
                    "tab": ["Magic"]
                },
                "PageNo": 1,
                "ClientGuid": "30c874915d164f71bf6f84f594bf623f",
                "IndexName": "",
                "ClientData": {
                    "VisitorId": ""
                },
                "query": f"(card\\ name.text: \"{self.cardName}\" OR card\\ name\\ 2.text: \"{self.cardName}\")"
                },
            headers={
                "authority": "essearchapi-na.hawksearch.com",
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "content-type": "application/json;charset=UTF-8",
                "origin": "https://www.facetofacegames.com",
                "pragma": "no-cache",
                "referer": "https://www.facetofacegames.com/",
                "sec-ch-ua": "\"Chromium\";v=\"106\", \"Google Chrome\";v=\"106\", \"Not;A=Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
            })
        # Load the response
        print('loading the response')
        data = json.loads(response.text)

        print("data:")
        print(data)