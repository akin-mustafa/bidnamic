from django.db.models import Case, DecimalField, F, QuerySet, When
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404

from bidnamic.search_terms.filters import SearchTermFilter
from bidnamic.search_terms.models import SearchTerm
from bidnamic.search_terms.serializers import (SearchTermSerializer,
                                               TopSearchesSerializer)


class SearchTermViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SearchTerm.objects.all()
    serializer_class = SearchTermSerializer
    filterset_class = SearchTermFilter


class CampaignTopSearchesView(generics.ListAPIView):
    queryset = SearchTerm.objects.all()
    serializer_class = TopSearchesSerializer
    filterset_class = SearchTermFilter

    def get_queryset(self) -> QuerySet:
        return self.queryset. \
            filter(campaign__structure_value=self.kwargs['structure_value']). \
            values('campaign__structure_value', 'search_term'). \
            annotate(
                roas=Case(
                    When(cost=0, then=0),
                    default=F('conversion_value') / F('cost'),
                    output_field=DecimalField(decimal_places=2, max_digits=10)
                )
            ).order_by('-roas')[:10]


class AdGroupTopSearchesView(CampaignTopSearchesView):

    def get_queryset(self) -> QuerySet:
        return self.queryset. \
            filter(ad_group__alias=self.kwargs['alias']). \
            values('ad_group__alias', 'search_term'). \
            annotate(
                roas=Case(
                    When(cost=0, then=0),
                    default=F('conversion_value') / F('cost'),
                    output_field=DecimalField(decimal_places=2, max_digits=10)
                )
            ).order_by('-roas')[:10]
