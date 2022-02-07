from django_filters import rest_framework as filters

from bidnamic.campaigns.models import Campaign


class CampaignFilter(filters.FilterSet):
    class Meta:
        model = Campaign
        fields = {
            "id": ["exact"],
            "structure_value": ["exact", "contains"],
            "status": ["exact"],
            "created_at": ["exact", "gt", "gte", "lt", "lte"],
            "updated_at": ["exact", "gt", "gte", "lt", "lte"],
        }
