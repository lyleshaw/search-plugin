import requests
import validators
from bs4 import BeautifulSoup
from fastapi import FastAPI, Path, Query
from starlette.middleware.cors import CORSMiddleware

from api.logger import logger

app = FastAPI(
    title="Search Plugin",
    description="Use this plugin whenever users want to get content from website or provided an URL or want to get "
                "some latest info. The plugin enables you to fetch and return the content of a provided URL, "
                "allowing the model to access and utilize information from the internet.",
    version="1.0.0",
    servers=[
        {"url": "https://search.aireview.tech/", "description": "Prod environment"},
    ],
    docs_url="/api/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_text(text_path):
    text = ""
    url = text_path
    if validators.url(url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/91.0.4472.124 Safari/537.36",}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text()
        else:
            raise ValueError(f"Invalid URL! Status code {response.status_code}.")
    text = " ".join(text.split())
    return text


# Path: /api/search
# Param: query: str
# Return: resp: str
@app.get("/api/search", description="You should generate URLs based on user input, such as creating a Google search "
                                    "URL (https://www.google.com/search?q={keyword}) to gather more information and "
                                    "assist users more effectively. For example, when a user asks for the Bitcoin "
                                    "price, you should send a HTTP request to "
                                    "https://coinmarketcap.com/currencies/bitcoin/ to retrieve the current price. If "
                                    "there is a URL, just send it.Only send URL link to this plugin.")
async def search(link: str = Query(description="request link")) -> str:
    logger.info("search start")
    logger.info("HTTP /search request: %s", link)
    text = get_text(link)

    logger.info("HTTP /search data: %s", text)
    return text


# start server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
