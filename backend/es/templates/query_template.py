from typing import List

from jinja2 import Template

from backend.models import SearchOptions, SearchRequest


class MatchAllQueryTemplate:
    query: str = """
    { "match_all": {}}
    """

    def render(self) -> str:
        return self.query


class SearchUIQueryTemplate:
    template: Template = Template(
        source="""
  {
    "bool": {
      "should": [
        {
          "multi_match": {
            "query": "{{ query.search_term }}",
            "fields": {{ fields | tojson }},
            "type": "best_fields",
            "operator": "and"
          }
        },
        {
          "multi_match": {
            "query": "{{ query.search_term }}",
            "fields": {{ fields | tojson }},
            "type": "cross_fields"
          }
        },
        {
          "multi_match": {
            "query": "{{ query.search_term }}",
            "fields": {{ fields | tojson }},
            "type": "phrase"
          }
        },
        {
          "multi_match": {
            "query": "{{ query.search_term }}",
            "fields": {{ fields | tojson }},
            "type": "phrase_prefix"
          }
        }
      ]
    }
  }
    """
    )

    def _fields(self, options: SearchOptions) -> List[str]:
        fields = []
        for field, value in options.search_fields.items():
            if value is not None and "weight" in value:
                weight: int = value["weight"]
                fields.append(f"{field}^{weight}")
            else:
                fields.append(f"{field}^1")
        return fields

    def render(self, request: SearchRequest) -> str:
        return self.template.render(query=request.query, fields=self._fields(request.options))
