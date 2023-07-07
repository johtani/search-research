import json
from typing import Any, Callable, Iterable, Mapping

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from backend.es.config import Config
from backend.indexer import IndexRepository


class EsIndexRepository(IndexRepository):
    config: Config
    esclient: Elasticsearch

    def __init__(self, config: Config):
        self.config = config
        self.esclient = Elasticsearch(config.url)

    def get_index_name(self):
        return self.config.index

    def create_index(self):
        schema = self.load_schema_from_file()
        self.esclient.indices.create(index=self.config.index, mappings=schema["mappings"], settings=schema["settings"])

    def load_schema_from_file(self) -> dict:
        with open(self.config.schema_path, "r") as config_file:
            schema = json.loads(config_file.read())
        return schema

    def is_exist_index(self) -> bool:
        return self.esclient.indices.exists(index=self.config.index).body

    def delete_index(self):
        self.esclient.indices.delete(index=self.config.index)

    def _update_index_settings(self, settings: Mapping[str, Any]):
        self.esclient.indices.put_settings(index=self.config.index, settings=settings)

    def _refresh(self):
        self.esclient.indices.refresh(index=self.config.index)

    def bulk_index(self, actions: Iterable[Any], progress: Callable) -> int:
        successes = 0
        settings: Mapping[str, Any] = {"index": {"refresh_interval": "-1"}}
        self._update_index_settings(settings=settings)
        for ok, action in streaming_bulk(client=self.esclient, index=self.get_index_name(), actions=actions):
            progress()
            successes += ok
        self._refresh()
        settings = {"index": {"refresh_interval": None}}
        self._update_index_settings(settings=settings)
        return successes
