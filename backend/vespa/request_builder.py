import logging

from jinja2 import Template

from backend.models import SearchOptions, SearchQuery
from backend.vespa.searcher import VespaRequest

logger = logging.getLogger(__file__)


class YQLTemplate:
    template: Template = Template(
        source="select {% for field in fields -%}{{field}}{%+ if not loop.last %}, {% endif %}{%- endfor %} from {{index}} where {{condition}}"
    )

    def _build_where_conditions(self, search_term: str) -> str:
        if len(search_term) > 0:
            return f"default contains {search_term}"
        else:
            # 条件指定なしという意味のtrue
            return "true"

    def render(self, index: str, fields: list[str], search_term: str) -> str:
        condition: str = self._build_where_conditions(search_term=search_term)
        if len(fields) > 0:
            return self.template.render(index=index, condition=condition, fields=fields).replace("\n", "")
        else:
            return self.template.render(index=index, condition=condition, fields=["*"]).replace("\n", "")


class GroupingTemplate:
    template: Template = Template(source="all(group({{field}}) order(-count()) each(output(count())))")

    def render(self, field: str) -> str:
        return self.template.render(field=field)


class GroupingAllTemplate:
    template: Template = Template(source="all({% for grouping in groupings %}{{grouping}} {% endfor %})")

    def render(self, facets: list[str]) -> str:
        if facets is None or len(facets) == 0:
            return ""
        else:
            grouping_template: GroupingTemplate = GroupingTemplate()
            groupings: list[str] = []
            for facet in facets:
                groupings.append(grouping_template.render(facet))
            return self.template.render(groupings=groupings)


class VespaRequestBuilder:
    hits: int
    offset: int
    fields: list[str]
    index: str
    search_term: str
    facets: list[str]
    yql_template: YQLTemplate
    grouping_template: GroupingAllTemplate

    def __init__(self, index: str):
        self.offset = 0
        self.hits = 0
        self.fields = []
        self.index = index
        self.search_term = ""
        self.facets = []
        self.yql_template = YQLTemplate()
        self.grouping_template = GroupingAllTemplate()

    def build(self) -> VespaRequest:
        req = VespaRequest(
            offset=self.offset,
            hits=self.hits,
            yql=self.yql_template.render(index=self.index, fields=self.fields, search_term=self.search_term),
            select=self.grouping_template.render(facets=self.facets),
        )
        return req

    def limit_offset(self, query: SearchQuery):
        self.offset = (query.current - 1) * query.results_per_page
        self.hits = query.results_per_page

    def summary_fields(self, options: SearchOptions):
        for field in options.result_fields.keys():
            self.fields.append(field)

    def conditions(self, query: SearchQuery):
        self.search_term = query.search_term

    def grouping(self, options: SearchOptions):
        # TODO need type?
        for facet in options.facets.keys():
            self.facets.append(facet)
