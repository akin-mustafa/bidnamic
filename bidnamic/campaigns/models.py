from django.db import models

from core.models.base_models import BaseAbstractModel
from core.models.enums import Statuses


class Campaign(BaseAbstractModel):
    id = models.PositiveBigIntegerField(primary_key=True)
    structure_value = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=Statuses.choices)

    class Meta:
        indexes = (models.Index(fields=["structure_value", "status"]),)

    def __str__(self):
        return f"{self.id}-{self.structure_value}-{self.status}"
