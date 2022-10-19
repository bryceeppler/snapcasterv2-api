from fastapi import FastAPI
from pydantic import BaseModel

class SingleCardSearch(BaseModel):
    cardName: str
    websites: list

app = FastAPI()

data = [
    {
        "id": 1,
        "name": 'Dockside Extortionist',
        "set": 'Core Set 2021',
        "price": 54.99,
        "image":
            'https://cards.scryfall.io/png/front/5/7/571bc9eb-8d13-4008-86b5-2e348a326d58.png?1615499802',
            "store": '401 Games',
            "condition": 'NM',
            "link": 'https://store.401games.ca/pages/search-results?q=dockside+extortionist',
    },
    {
        "id": 2,
        "name": 'Dockside Extortionist',
        "set": 'Core Set 2021',
        "price": 54.99,
        "image":
            'https://cards.scryfall.io/png/front/5/7/571bc9eb-8d13-4008-86b5-2e348a326d58.png?1615499802',
            "store": '401 Games',
            "condition": 'NM',
            "link": 'https://store.401games.ca/pages/search-results?q=dockside+extortionist',
    },
    {
        "id": 3,
        "name": 'Dockside Extortionist',
        "set": 'Core Set 2021',
        "price": 54.99,
        "image":
            'https://cards.scryfall.io/png/front/5/7/571bc9eb-8d13-4008-86b5-2e348a326d58.png?1615499802',
            "store": '401 Games',
            "condition": 'NM',
            "link": 'https://store.401games.ca/pages/search-results?q=dockside+extortionist',
    },
    {
        "id": 4,
        "name": 'Dockside Extortionist',
        "set": 'Core Set 2021',
        "price": 54.99,
        "image":
            'https://cards.scryfall.io/png/front/5/7/571bc9eb-8d13-4008-86b5-2e348a326d58.png?1615499802',
            "store": '401 Games',
            "condition": 'NM',
            "link": 'https://store.401games.ca/pages/search-results?q=dockside+extortionist',
    },
    {
        "id": 5,
        "name": 'Dockside Extortionist',
        "set": 'Core Set 2021',
        "price": 54.99,
        "image":
            'https://cards.scryfall.io/png/front/5/7/571bc9eb-8d13-4008-86b5-2e348a326d58.png?1615499802',
            "store": '401 Games',
            "condition": 'NM',
            "link": 'https://store.401games.ca/pages/search-results?q=dockside+extortionist',
    },
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/search/single/")
async def search_single(request: SingleCardSearch):
    print(request.cardName)
    print(request.websites)

    return data
    return {"message": f"success"}
