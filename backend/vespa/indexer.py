from pathlib import Path
from typing import Any, Callable, Iterable

from vespa.application import Vespa
from vespa.deployment import VespaDeployment

from backend.indexer import IndexRepository
from backend.vespa.config import Config


class VespaServer(VespaDeployment):
    def __init__(self):
        pass

    def deploy(self, application_root: Path):
        pass


class VespaIndexRepository(IndexRepository):
    config: Config
    client: Vespa

    def __init__(self, config: Config) -> None:
        self.config = config
        self.client = Vespa(url=self.config.document_url)

    def get_index_name(self):
        return self.config.index

    def create_index(self):
        # deploy application package
        pass

    def is_exist_index(self) -> bool:
        # どうやって取得するんだろう？できない？？
        return False

    def delete_index(self):
        # これもできない？
        pass

    def bulk_index(self, actions: Iterable[Any], progress: Callable[..., Any]):
        feed_data = []
        for doc in actions:
            feed_data.append(doc)
            progress()
        results = self.client.feed_batch(batch=feed_data, schema=self.config.index, output=False)
        return len(results)
