from django.db.models import Case, DecimalField, F, When
from django.test import TestCase

from bidnamic.search_terms.models import SearchTerm


class ModelTestCase(TestCase):
    def test_manager(self):
        data = {"campaign__structure_value": "test"}
        self.assertEqual(
            str(SearchTerm.objects.get_top_searches(**data).query),
            str(
                SearchTerm.objects.filter(**data)
                .values("search_term", *data.keys())
                .annotate(
                    roas=Case(
                        When(cost=0, then=0),
                        default=F("conversion_value") / F("cost"),
                        output_field=DecimalField(decimal_places=2, max_digits=10),
                    )
                )
                .order_by("-roas")[:10]
                .query
            ),
        )
