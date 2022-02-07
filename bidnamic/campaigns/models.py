from django.apps import apps
from django.db import models
from django.db.models import Case, DecimalField, F, When

from core.models.base_models import BaseAbstractModel
from core.models.enums import Statuses


class Campaign(BaseAbstractModel):
    id = models.PositiveBigIntegerField(primary_key=True)
    structure_value = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=Statuses.choices)

    class Meta:
        indexes = (
            models.Index(fields=['structure_value', 'status']),
        )

    def __str__(self):
        return f'{self.id}-{self.structure_value}-{self.status}'

    def top10_searches(self):
        SearchTerm = apps.get_model('search_terms', 'SearchTerm')   # NOQA
        return SearchTerm.objects.filter(campaign_id=self.id).\
            values('campaign_id', 'search_term'). \
            annotate(
                roas=Case(
                    When(cost=0, then=0),
                    default=F('conversion_value') / F('cost'),
                    output_field=DecimalField(decimal_places=2, max_digits=10)
                )
            ).order_by('-roas')[:10]
