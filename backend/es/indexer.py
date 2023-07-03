from elasticsearch import Elasticsearch
import json

import backend
from backend.es.config import Config


class EsIndexer:
    config: Config
    esclient: Elasticsearch

    def __init__(self, config: Config):
        self.config = config
        self.esclient = Elasticsearch(
            config.url
        )

    def create_index(self):
        schema = self.load_schema_from_file()
        self.esclient.indices.create(
            index=self.config.index,
            mappings=schema["mappings"],
            settings=schema["settings"]
        )

    def load_schema_from_file(self) -> dict:
        with open(self.config.schema_path, "r") as config_file:
            schema = json.loads(config_file.read())
        return schema


    def is_exist_index(self) -> bool:
        return self.esclient.indices.exists(index=self.config.index)

    def delete_index(self):
        self.esclient.indices.delete(index=self.config.index)
