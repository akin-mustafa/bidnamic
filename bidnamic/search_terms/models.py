from django.db import models

from bidnamic.ad_groups.models import AdGroup
from bidnamic.campaigns.models import Campaign
from bidnamic.search_terms.managers import SearchTermQuerySet
from core.models.base_models import BaseAbstractModel


class SearchTerm(BaseAbstractModel):
    date = models.DateField()
    ad_group = models.ForeignKey(AdGroup, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    clicks = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    conversion_value = models.DecimalField(decimal_places=2, max_digits=10)
    conversions = models.PositiveIntegerField()
    search_term = models.CharField(max_length=250)
    objects = models.Manager.from_queryset(SearchTermQuerySet)()

    class Meta:
        indexes = (
            models.Index(fields=["search_term"]),
            models.Index(fields=["date", "search_term"]),
        )

    def __str__(self):
        return (
            f"{self.campaign_id}-{self.ad_group_id}-"
            f"{self.search_term}-{self.date}"
        )
