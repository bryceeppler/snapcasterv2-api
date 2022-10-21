from bs4 import BeautifulSoup
import requests
import json
from .Scraper import Scraper

class EverythingGamesScraper(Scraper):
    """
    Everything games uses a completely exposed API to get the stock of cards
    We can literally hit the API and get all the information we need
    """
    def __init__(self, cardName):
        Scraper.__init__(self, cardName)
        self.siteUrl = 'https://www.everythinggames.ca'
        self.baseUrl = 'https://www.everythinggames.ca/search?search='
        self.url = self.createUrl()
        self.website = 'everythinggames'
    
    def createUrl(self):
        url = ""
        return url

    def scrape(self):
        pass