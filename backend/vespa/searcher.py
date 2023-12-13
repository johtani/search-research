from dataclasses import asdict, dataclass, field
from typing import Dict, List

from dataclasses_json import DataClassJsonMixin, config
from vespa.application import Vespa
from vespa.io import VespaQueryResponse

from backend.vespa.config import Config


@dataclass
class VespaRequest(DataClassJsonMixin):
    yql: str = ""
    hits: int = 20
    offset: int = 0
    type_: str = field(metadata=config(field_name="type"), default="all")
    ranking: str = ""
    select: str = ""


@dataclass
class VespaResponse:
    orig_res: VespaQueryResponse

    def __init__(self, orig_res):
        self.orig_res = orig_res

    @property
    def number_of_hits(self) -> int:
        return self.orig_res.number_documents_retrieved

    @property
    def hits(self) -> List[Dict]:
        return self.orig_res.hits


class VespaSearchRepository:
    config: Config
    client: Vespa

    def __init__(self, config: Config) -> None:
        self.config = config
        self.client = Vespa(url=self.config.document_url)

    def search(self, request: VespaRequest) -> VespaResponse:
        vespa_q_res = self.client.query(body=asdict(request))
        # TODO need to copy...
        return VespaResponse(vespa_q_res)

    def autocomplete(self, request):
        pass
