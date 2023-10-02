import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.es.search_engine_translator import EsTranslator
from backend.models import SearchRequest
from backend.search_engine_translator import SearchEngineTranslator

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

_translators: dict[str, SearchEngineTranslator] = {"es": EsTranslator()}


@app.post("/search")
async def search(request: SearchRequest):
    logger.debug(f"{request=}")
    translator = _translators["es"]
    return translator.translate_and_search(request)


@app.post("/autocomplete")
async def autocomplete():
    return {"hoge": "fuga"}
