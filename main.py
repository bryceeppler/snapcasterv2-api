from fastapi import FastAPI
from pydantic import BaseModel
import concurrent.futures
from fastapi.middleware.cors import CORSMiddleware

# Scrapers
from scrapers.base.GauntletScraper import GauntletScraper
from scrapers.base.Four01Scraper import Four01Scraper
from scrapers.base.FusionScraper import FusionScraper
from scrapers.base.KanatacgScraper import KanatacgScraper
from scrapers.base.HouseOfCardsScraper import HouseOfCardsScraper
from scrapers.base.EverythingGamesScraper import EverythingGamesScraper
from scrapers.base.MagicStrongholdScraper import MagicStrongholdScraper
from scrapers.base.FaceToFaceScraper import FaceToFaceScraper

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
    }

    print("request.websites", request.websites)

    # Filter out scrapers that are not requested in request.websites
    try:
        scrapers = [scraperMap[website] for website in request.websites]
    except KeyError:
        return {"error": "Invalid website provided"}
    
    # scrapers = [
    #     everythingGamesScraper,
    #     four01Scraper,
    #     fusionScraper,
    #     kanatacgScraper,
    #     gauntletScraper,      
    # ]

    # Run scrapers in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        threadResults = executor.map(transform, scrapers)

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
    results = []

    # Scraper function
    def transform(scraper):
        scraper.scrape()
        scraperResults = scraper.getResults()
        for result in scraperResults:
            results.append(result)
        return

    # Arrange scrapers
    houseOfCardsScraper = HouseOfCardsScraper(cardNames)
    gauntletScraper = GauntletScraper(cardNames)
    kanatacgScraper = KanatacgScraper(cardNames)
    fusionScraper = FusionScraper(cardNames)
    four01Scraper = Four01Scraper(cardNames)
    everythingGamesScraper = EverythingGamesScraper(cardNames)
    magicStrongholdScraper = MagicStrongholdScraper(cardNames)
    faceToFaceScraper = FaceToFaceScraper(cardNames)

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
    } 

    return {"message": "Hello World"}

