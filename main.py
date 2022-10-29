from fastapi import FastAPI
from pydantic import BaseModel
import concurrent.futures
from fastapi.middleware.cors import CORSMiddleware
# import datetime
from datetime import datetime

# Scrapers
from scrapers.base.GauntletScraper import GauntletScraper
from scrapers.base.Four01Scraper import Four01Scraper
from scrapers.base.FusionScraper import FusionScraper
from scrapers.base.KanatacgScraper import KanatacgScraper
from scrapers.base.HouseOfCardsScraper import HouseOfCardsScraper
from scrapers.base.EverythingGamesScraper import EverythingGamesScraper
from scrapers.base.MagicStrongholdScraper import MagicStrongholdScraper
from scrapers.base.FaceToFaceScraper import FaceToFaceScraper
from scrapers.base.ConnectionGamesScraper import ConnectionGamesScraper
from scrapers.base.SequenceScraper import SequenceScraper
from scrapers.base.TopDeckHeroScraper import TopDeckHeroScraper
from scrapers.base.Jeux3DragonsScraper import Jeux3DragonsScraper
from scrapers.base.AtlasScraper import AtlasScraper
from scrapers.base.GamezillaScraper import GamezillaScraper
from scrapers.base.HairyTScraper import HairyTScraper
from scrapers.base.ExorGamesScraper import ExorGamesScraper
from scrapers.base.GameKnightScraper import GameKnightScraper
from scrapers.base.EnterTheBattlefieldScraper import EnterTheBattlefieldScraper
from scrapers.base.ManaforceScraper import ManaforceScraper
from db.database import engine, SQLModel, Session
from db.models import Search


# Pydantic Models


class SingleCardSearch(BaseModel):
    cardName: str
    websites: list

class BulkCardSearch(BaseModel):
    cardNames: list
    websites: list
    worstCondition: str

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://snapcasterv2-client.vercel.app",
    "https://snapcaster.bryceeppler.com",
    "https://www.snapcaster.ca",
    "https://snapcaster.ca",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/search/single/")
async def search_single(request: SingleCardSearch):
    """
    Search for a single card and return all prices across the provided websites
    """
    # List to store results from all threads
    results = []

    # Scraper function
    def transform(scraper):
        scraper.scrape()
        scraperResults = scraper.getResults()
        for result in scraperResults:
            results.append(result)
        return

    # Arrange scrapers
    houseOfCardsScraper = HouseOfCardsScraper(request.cardName)
    gauntletScraper = GauntletScraper(request.cardName)
    kanatacgScraper = KanatacgScraper(request.cardName)
    fusionScraper = FusionScraper(request.cardName)
    four01Scraper = Four01Scraper(request.cardName)
    everythingGamesScraper = EverythingGamesScraper(request.cardName)
    magicStrongholdScraper = MagicStrongholdScraper(request.cardName)
    faceToFaceScraper = FaceToFaceScraper(request.cardName)
    connectionGamesScraper = ConnectionGamesScraper(request.cardName)
    topDeckHeroScraper = TopDeckHeroScraper(request.cardName)
    jeux3DragonsScraper = Jeux3DragonsScraper(request.cardName)
    sequenceScraper = SequenceScraper(request.cardName)
    atlasScraper = AtlasScraper(request.cardName)
    hairyTScraper = HairyTScraper(request.cardName)
    gamezillaScraper = GamezillaScraper(request.cardName)
    exorGamesScraper = ExorGamesScraper(request.cardName)
    gameKnightScraper = GameKnightScraper(request.cardName)
    enterTheBattlefieldScraper = EnterTheBattlefieldScraper(request.cardName)
    manaforceScraper = ManaforceScraper(request.cardName)



    # Map scrapers to an identifier keyword
    scraperMap = {
        "houseofcards": houseOfCardsScraper,
        "gauntlet": gauntletScraper,
        "kanatacg": kanatacgScraper,
        "fusion": fusionScraper,
        "four01": four01Scraper,
        "everythinggames": everythingGamesScraper,
        "magicstronghold": magicStrongholdScraper,
        "facetoface": faceToFaceScraper,
        "connectiongames": connectionGamesScraper,
        "topdeckhero": topDeckHeroScraper,
        "jeux3dragons": jeux3DragonsScraper,
        'sequencegaming': sequenceScraper,
        'atlas': atlasScraper,
        'hairyt': hairyTScraper,
        'gamezilla': gamezillaScraper,
        'exorgames': exorGamesScraper,
        'gameknight': gameKnightScraper,
        'enterthebattlefield': enterTheBattlefieldScraper,
        'manaforce': manaforceScraper

    }


    # Filter out scrapers that are not requested in request.websites
    try:
        # if "all" in request.websites: then we want all scrapers
        if "all" in request.websites:
            scrapers = scraperMap.values()
        else:
            scrapers = [scraperMap[website] for website in request.websites]
    except KeyError:
        return {"error": "Invalid website provided"}
    
    # scrapers = [
    #     connectionGamesScraper      
    # ]

    # Run scrapers in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        threadResults = executor.map(transform, scrapers)

    # Create a new search object
    # post a log to the database
    numResults = len(results)
    log = Search(query=request.cardName, websites=','.join(request.websites), queryType="single", results="", numResults=numResults, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    session.add(log)
    session.commit()
    session.close()

    return results
    
@app.post("/search/bulk/")
async def search_bulk(request: BulkCardSearch):
    """
    Search for a list of cards and return all prices across the provided websites
    """
    # CardObject = {
    #    "cardName": "cardName",
    #   "variants": []
    # }

    # For each card in the list, we want to run the single card search
    # then we want to return an array of cardObjects

    cardNames = request.cardNames
    websites = request.websites
    worstCondition = request.worstCondition
    
    # List to store results from all threads
    totalResults = []
    results = {}

    # Scraper function
    def transform(scraper):
        scraper.scrape()
        scraperResults = scraper.getResults()
        for result in scraperResults:
            if result['name'].lower() in results:
                results[result['name'].lower()].append(result)
            else:
                results[result['name'].lower()] = [result]

        return

    def executeScrapers(cardName):
        # For each card 
        # Arrange scrapers
        houseOfCardsScraper = HouseOfCardsScraper(cardName)
        gauntletScraper = GauntletScraper(cardName)
        kanatacgScraper = KanatacgScraper(cardName)
        fusionScraper = FusionScraper(cardName)
        four01Scraper = Four01Scraper(cardName)
        everythingGamesScraper = EverythingGamesScraper(cardName)
        magicStrongholdScraper = MagicStrongholdScraper(cardName)
        faceToFaceScraper = FaceToFaceScraper(cardName)
        connectionGamesScraper = ConnectionGamesScraper(cardName)
        topDeckHeroScraper = TopDeckHeroScraper(cardName)
        jeux3DragonsScraper = Jeux3DragonsScraper(cardName)
        sequenceScraper = SequenceScraper(cardName)
        atlasScraper = AtlasScraper(cardName)
        hairyTScraper = HairyTScraper(cardName)
        gamezillaScraper = GamezillaScraper(cardName)
        exorGamesScraper = ExorGamesScraper(cardName)
        gameKnightScraper = GameKnightScraper(cardName)
        enterTheBattlefieldScraper = EnterTheBattlefieldScraper(cardName)
        manaforceScraper = ManaforceScraper(cardName)

        # Map scrapers to an identifier keyword
        scraperMap = {
            "houseofcards": houseOfCardsScraper,
            "gauntlet": gauntletScraper,
            "kanatacg": kanatacgScraper,
            "fusion": fusionScraper,
            "four01": four01Scraper,
            "everythinggames": everythingGamesScraper,
            "magicstronghold": magicStrongholdScraper,
            "facetoface": faceToFaceScraper,
            "connectiongames": connectionGamesScraper,
            'topdeckhero': topDeckHeroScraper,
            'jeux3dragons': jeux3DragonsScraper,
            'sequencegaming': sequenceScraper,
            'atlas': atlasScraper,
            'hairyt': hairyTScraper,
            'gamezilla': gamezillaScraper,
            'exorgames': exorGamesScraper,
            'gameknight': gameKnightScraper,
            'enterthebattlefield': enterTheBattlefieldScraper,
            'manaforce': manaforceScraper
        }

        # Filter out scrapers that are not requested in request.websites
        try:
            scrapers = [scraperMap[website] for website in websites]
        except KeyError:
            return {"error": "Invalid website provided"}
        
        # Run scrapers in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            threadResults = executor.map(transform, scrapers)

        # Create a CardObject for the card
        cardObject = {
            "cardName": cardName.lower(),
            "variants": results[cardName.lower()]
        }
        totalResults.append(cardObject)
        return

    # Run the scrapers for each card in cardNames, then create a CardObject for it
    # and add it to the results array
    # for cardName in cardNames:
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        threadResults = executor.map(executeScrapers, cardNames)

    # post a log to the database
    # numResults = the length of the variant array in all card objects
    numResults = 0
    for card in totalResults:
        numResults += len(card['variants'])

    log = Search(query=','.join(request.cardNames), websites=','.join(request.websites), queryType="multi", results="", numResults=numResults, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    session.add(log)
    session.commit()
    session.close()

    return totalResults

# log search queries in database
@app.post("/log/")
async def log(request: Search):
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    session.add(request)
    session.commit()
    session.close()
    return {"message": "Logged"}
