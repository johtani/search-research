from dataclasses import asdict, dataclass, field

from dataclasses_json import DataClassJsonMixin, config
from vespa.application import Vespa

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
    def __init__(self, orig_res):
        pass


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
