from rest_framework import viewsets

from bidnamic.ad_groups.filters import AdGroupFilter
from bidnamic.ad_groups.models import AdGroup
from bidnamic.ad_groups.serializers import AdGroupSerializer


class AdGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdGroup.objects.all()
    filterset_class = AdGroupFilter
    serializer_class = AdGroupSerializer
