from decimal import Decimal

from django.db import models
from django.db.models import F, QuerySet, Sum
from django.db.models.functions import Coalesce, NullIf


class SearchTermQuerySet(models.QuerySet):
    def get_top_searches(self, field) -> QuerySet:
        annotation_map = {
            "campaign__structure_value": {
                "structure_value": F("campaign__structure_value")
            },
            "ad_group__alias": {
                "alias": F("ad_group__alias")
            }
        }
        return (
            self.values("search_term", field)
            .annotate(
                roas=Coalesce(
                    Sum(F('conversion_value'))
                    / NullIf(
                        Sum(F('cost')),
                        Decimal('0.00')
                    ), Decimal('0.00')
                ),
                total_cost=Sum("cost"),
                total_conversion_value=Sum("conversion_value"),
                **annotation_map[field],
            )
            .order_by("-roas")[:10]
        )
