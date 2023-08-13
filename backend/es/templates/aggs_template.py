from typing import Dict

from jinja2 import Template

from backend.models import Filter, SearchOptions


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
            facets.append(self.terms_template.render(bucket=bucket, config=config))
        return self.template.render(facets=facets)


class BucketAllWithFilterTemplate:
    template: Template = Template(
        source="""
        {
          "facet_bucket_all": {
            "aggs": {},
            "filter": { "bool": { "must": [
                {% for name, post_filter in post_filters.items() %}
                {{ post_filter }}
                {% if not loop.last %}
                ,
                {% endif %}
                {% endfor %}
            ] } }
          }
          {% for bucket, facet in facets.items() %}
          {% if loop.first %}
          ,
          {% endif %}
          "facet_bucket_{{ bucket }}": {
            "aggs": {
              {{ facet }}
            },
            "filter": {
              "bool": {
                "must": [
                  {% for name, post_filter in post_filters.items() if name != bucket %}
                  {{ post_filter }}
                  {% if not loop.last %}
                  ,
                  {% endif %}
                  {% endfor %}
                ]
              }
            }
          }
          {% if not loop.last %}
          ,
          {% endif %}
          {% endfor %}
        }
        """
    )
    terms_template = TermsAggTemplate()

    def render(self, post_filters: dict[str, str], options: SearchOptions) -> str:
        facets: dict[str, str] = {}
        for bucket, config in options.facets.items():
            facets[bucket] = self.terms_template.render(bucket=bucket, config=config)
        return self.template.render(facets=facets, post_filters=post_filters)


class FilterTemplate:
    template: Template = Template(
        source="""
    {
      "bool": {
        "should": [
          {% for value in filter.values %}
          { "term": { "{{ filter.field }}": "{{ value }}" } }
          {% if not loop.last %}
          ,
          {% endif %}
          {% endfor %}
        ]
      }
    }
    """
    )

    def render(self, filter: Filter) -> str:
        return self.template.render(filter=filter)


class PostFilterTemplate:
    template: Template = Template(
        source="""
    {
    "bool": {
      "must": [
        {% for filter in filters %}
        {{ filter }}
        {% if not loop.last %}
        ,
        {% endif %}
        {% endfor %}
      ]
    }
  }
    """
    )

    def render(self, filters: Dict[str, str]) -> str:
        return self.template.render(filters=filters.values())
