import requests
import validators
from bs4 import BeautifulSoup
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.logger import logger

app = FastAPI(
    title="Search Plugin",
    description="This tool allows users to provide a URL(or URLs) "
                "and optionally requests for interacting with, extracting specific information or how to do "
                "with the content from the URL. Requests may include rewrite, translate, and others. "
                "If there any requests, when accessing the /api/visit-web endpoint, the parameter 'user_has_request' "
                "should be set to 'true. And if there's no any requests, 'user_has_request' should be set to 'false'.",
    version="1.0.0",
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
@app.get("/api/search", description="if there is any keyword that can be searched in google, give them to me in "
                                    "user's word only without any additional words, then link should be like "
                                    "'https://www.google.com/search?q={keyword}'. If there is a URL, the link should "
                                    "be this URL")
async def search(link: str) -> str:
    logger.info("search start")
    logger.info("HTTP /search request: %s", link)
    text = get_text(link)

    logger.info("HTTP /search data: %s", text)
    return text


# start server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
