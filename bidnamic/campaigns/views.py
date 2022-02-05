from rest_framework import viewsets

from bidnamic.campaigns.filters import CampaignsFilter
from bidnamic.campaigns.models import Campaign
from bidnamic.campaigns.serializers import CampaignSerializer


class CampaignViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Campaign.objects.all()
    filterset_class = CampaignsFilter
    serializer_class = CampaignSerializer
