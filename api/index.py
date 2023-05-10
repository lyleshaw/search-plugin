from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.google_search import get_serps
from api.logger import logger

app = FastAPI(
    title="Google Search Plugin",
    description="Plugin for searching through internet to find answers to questions and retrieve relevant information."
                "Use it whenever a user asks something that might be found in Google or users ask to visit a website.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Path: /api/search
# Param: query: str
# Return: resp: str
@app.get("/api/query", description="Search for query, return search results in string.")
async def search(query: str) -> str:
    logger.info("search start")
    logger.info("HTTP /search request: %s", query)
    max_lengh = 1000
    try:
        data = get_serps(query, domain="google.com", host_language="zh-CN")
        resp = "search results as follow:\n"
        if data:
            for i in data:
                resp += "Title: " + i['title'] + "Text: " + i["text"] + "\n"
                if len(resp) > max_lengh:
                    break
        print(resp)
    except Exception as e:
        logger.error("search error: %s", e)
        return "Something went wrong."
    logger.info("HTTP /search data: %s", resp)
    return resp


# start server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
