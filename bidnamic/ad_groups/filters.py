from django_filters import rest_framework as filters

from bidnamic.ad_groups.models import AdGroup


class AdGroupFilter(filters.FilterSet):
    class Meta:
        model = AdGroup
        fields = {
            "id": ["exact"],
            "campaign_id": ["exact"],
            "alias": ["exact", "contains"],
            "status": ["exact"],
            "created_at": ["exact", "gt", "gte", "lt", "lte"],
            "updated_at": ["exact", "gt", "gte", "lt", "lte"],
        }
