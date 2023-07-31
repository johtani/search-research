import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models import SearchRequest
from backend.search_engine_translator import EsTranslator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["OPTIONS", "HEAD", "GET", "POST", "PUT", "DELETE"],
    allow_headers=[
        "X-Requested-With",
        "X-Auth-Token",
        "Content-Type",
        "Content-Length",
        "Authorization",
        "Access-Control-Allow-Headers",
        "Accept",
        "x-elastic-client-meta",
    ],
)

logger = logging.getLogger("uvicorn")


translator = EsTranslator()


@app.post("/search")
async def search(request: SearchRequest):
    logger.info(f"{request=}")
    return translator.translate_and_search(request)


@app.post("/autocomplete")
async def autocomplete():
    return {"hoge": "fuga"}
