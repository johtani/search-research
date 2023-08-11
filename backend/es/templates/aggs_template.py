from typing import Dict

from jinja2 import Template

from backend.models import SearchOptions


class TermsAggTemplate:
    template: Template = Template(
        source="""
        "{{ bucket }}": {
          "terms": {
            "field": "{{ bucket }}",
            {% if config['size'] %}
            "size": {{ config.size }},
            {% else %}
            "size": 20,
            {% endif %}
            {% if config['sort']%}
              {% if config['sort']['count'] %}
            "order": { "_count": "{{ config['sort']['count'] }}" }
              {% elif config['sort']['key'] %}
            "order": { "_key": "{{ config['sort']['key'] }}" }
              {% else %}
            "order": { "_count": "desc" }
              {% endif %}
            {% else %}
            "order": { "_count": "desc" }
            {% endif %}
          }
        }
        """
    )

    def render(self, bucket: str, config: Dict[str, str | int]) -> str:
        return self.template.render(bucket=bucket, config=config)


class BucketAllTemplate:
    template: Template = Template(
        source="""
        {
          "facet_bucket_all": {
            "aggs": {
                {% for facet in facets %}
                {{ facet }}
                {% if not loop.last %}
                ,
                {% endif %}
                {% endfor %}
            },
            "filter": { "bool": { "must": [] } }
          }
        }
        """
    )
    terms_template = TermsAggTemplate()

    def render(self, options: SearchOptions) -> str:
        facets = []
        for bucket, config in options.facets.items():
            facets.append(self.terms_template.render(bucket, config))
        return self.template.render(facets=facets)
