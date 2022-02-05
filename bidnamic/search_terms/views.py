from rest_framework import viewsets

from bidnamic.search_terms.filters import SearchTermFilter
from bidnamic.search_terms.models import SearchTerm
from bidnamic.search_terms.serializers import SearchTermSerializer


class SearchTermViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SearchTerm.objects.all()
    serializer_class = SearchTermSerializer
    filterset_class = SearchTermFilter
