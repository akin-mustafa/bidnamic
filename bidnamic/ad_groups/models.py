from django.db import models

from bidnamic.campaigns.models import Campaign
from core.models.enums import Statuses
from core.models.base_models import BaseAbstractModel


class AdGroup(BaseAbstractModel):
    id = models.PositiveBigIntegerField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    alias = models.CharField(max_length=250)
    status = models.CharField(max_length=10, choices=Statuses.choices)

    class Meta:
        indexes = (
            models.Index(fields=['alias', 'status']),
        )

