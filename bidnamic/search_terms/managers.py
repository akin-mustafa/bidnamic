from typing import Any

from django.db import models
from django.db.models import Case, DecimalField, F, QuerySet, When


class SearchTermQuerySet(models.QuerySet):
    def get_top_searches(self, **kwargs: dict[str, Any]) -> QuerySet:
        return (
            self.filter(**kwargs)
            .values("search_term", *kwargs.keys())
            .annotate(
                roas=Case(
                    When(cost=0, then=0),
                    default=F("conversion_value") / F("cost"),
                    output_field=DecimalField(decimal_places=2, max_digits=10),
                )
            )
            .order_by("-roas")[:10]
        )
