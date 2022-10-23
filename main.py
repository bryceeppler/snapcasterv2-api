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

# Pydantic Models


class SingleCardSearch(BaseModel):
    cardName: str
    websites: list


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


    # Map scrapers to an identifier keyword
    scraperMap = {
        "houseofcards": houseOfCardsScraper,
        "gauntlet": gauntletScraper,
        "kanatacg": kanatacgScraper,
        "fusion": fusionScraper,
        "four01": four01Scraper,
        "everythinggames": everythingGamesScraper,
        "magicstronghold": magicStrongholdScraper,
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

    # Right now we have asublist on each card edition of the stock and price
    # for each condition, but we want one list entry for each condition

    # We will need to refactor the scrapers in the future and we can remove this 
    # refomatting step

    # Join all results into one list
    # Each entry must have a unique id
    # joinedResults = []
    # for result in results:
    #     for entry in result:
    #         for stock in entry["stock"]:
    #             joinedResults.append({
    #                 "name": entry["name"],
    #                 "set": entry["set"],
    #                 "image": entry["image"],
    #                 "link": entry["link"],
    #                 "website": entry["website"],
    #                 "condition": stock["condition"],
    #                 "price": stock["price"],
    #                 "id": len(joinedResults) + 1
    #             })

    # join all lists into one list


    return results

