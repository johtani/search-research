from abc import abstractmethod

from backend.models import SearchRequest, SearchResult


class SearchEngineTranslator:
    @abstractmethod
    def translate_and_search(self, request: SearchRequest) -> SearchResult:
        pass
