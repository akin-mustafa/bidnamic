from django_filters import rest_framework as filters

from bidnamic.search_terms.models import SearchTerm


class SearchTermFilter(filters.FilterSet):
    class Meta:
        model = SearchTerm
        fields = {
            "id": ["exact"],
            "search_term": ["exact", "contains"],
            "ad_group_id": ["exact"],
            "campaign_id": ["exact"],
            "clicks": ["gt", "gte", "lt", "lte"],
            "cost": ["gt", "gte", "lt", "lte"],
            "conversion_value": ["gt", "gte", "lt", "lte"],
            "conversions": ["gt", "gte", "lt", "lte"],
            "date": ["exact", "gt", "gte", "lt", "lte"],
            "created_at": ["exact", "gt", "gte", "lt", "lte"],
            "updated_at": ["exact", "gt", "gte", "lt", "lte"],
        }
