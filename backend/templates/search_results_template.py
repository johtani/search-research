from typing import Any, Dict, List, TypedDict

from jinja2 import Template


class Field(TypedDict):
    raw: str | None
    snippets: List[str] | None


class DocFields(TypedDict):
    id: str
    raw: Any | None
    fields: Dict[str, Field] | None


class DocTemplate:
    template: Template = Template(
        source="""
    {
      "id": {
        "raw": "{{ id }}"
      },
      "_meta": {
        "id": "{{ id }}",
        "rawHit": {{ raw|tojson }}
      },
      {% for key, value in fields.items() %}
      "{{ key }}": {
        {% if value['snippets'] %}
        "snippet": {{ value.snippets|tojson }}
        {% elif value['raw'] %}
        "raw": "{{ value.raw }}"
        {% endif %}
      }
      {% if not loop.last %}
      ,
      {% endif %}
      {% endfor %}
    }
        """
    )

    def render(self, doc: DocFields) -> str:
        return self.template.render(id=doc["id"], raw=doc["raw"], fields=doc["fields"])
