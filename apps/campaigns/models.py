from django.db import models

from core.models.enums import Statuses
from core.models.base_models import BaseAbstractModel


class Campaign(BaseAbstractModel):
    id = models.PositiveBigIntegerField(primary_key=True)
    structure_value = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=Statuses.choices)
