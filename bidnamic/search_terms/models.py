from django.db import models

from bidnamic.ad_groups.models import AdGroup
from bidnamic.campaigns.models import Campaign
from core.models.base_models import BaseAbstractModel


class SearchTerm(BaseAbstractModel):
    date = models.DateField()
    ad_group_id = models.ForeignKey(AdGroup, on_delete=models.SET_NULL)
    campaign_id = models.ForeignKey(Campaign, on_delete=models.SET_NULL)
    clicks = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(decimal_places=2)
    conversion_value = models.DecimalField(decimal_places=2)
    conversions = models.PositiveIntegerField()
    search_term = models.CharField(max_length=250)
