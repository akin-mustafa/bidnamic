from django.db.models import QuerySet
from rest_framework import generics, viewsets

from bidnamic.search_terms.filters import SearchTermFilter
from bidnamic.search_terms.models import SearchTerm
from bidnamic.search_terms.serializers import (
    SearchTermSerializer,
    TopSearchesSerializer,
)


class SearchTermViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SearchTerm.objects
    serializer_class = SearchTermSerializer
    filterset_class = SearchTermFilter


class CampaignTopSearchesView(generics.ListAPIView):
    queryset = SearchTerm.objects.all()
    serializer_class = TopSearchesSerializer
    filterset_class = SearchTermFilter

    def get_queryset(self) -> QuerySet:
        return self.queryset.get_top_searches("campaign__structure_value")


class AdGroupTopSearchesView(CampaignTopSearchesView):
    def get_queryset(self) -> QuerySet:
        return self.queryset.get_top_searches("ad_group__alias")
