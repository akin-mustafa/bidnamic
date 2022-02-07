from django.db import models

from bidnamic.campaigns.models import Campaign
from core.models.base_models import BaseAbstractModel
from core.models.enums import Statuses


class AdGroup(BaseAbstractModel):
    id = models.PositiveBigIntegerField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    alias = models.CharField(max_length=250)
    status = models.CharField(max_length=10, choices=Statuses.choices)

    class Meta:
        indexes = (models.Index(fields=["alias", "status"]),)

    def __str__(self):
        return f"{self.id}-{self.campaign_id}-{self.alias}-{self.status}"
