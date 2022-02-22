import math

import pandas as pd
from django.conf import settings
from django.test import TestCase

from bidnamic.ad_groups.tasks import get_ad_groups
from bidnamic.campaigns.tasks import get_campaigns
from bidnamic.search_terms.models import SearchTerm
from bidnamic.search_terms.tasks import get_search_terms


class ModelTestCase(TestCase):
    def setUp(self) -> None:
        app_dir = settings.APPS_DIR / "utils/tests/data_files"
        self.campaign_file_path = app_dir / "campaigns.csv"
        self.ad_group_file_path = app_dir / "adgroups.csv"
        self.search_term_file_path = app_dir / "search_terms.csv"

    def test_manager(self):
        df = pd.read_csv(self.search_term_file_path).drop_duplicates()

        get_campaigns(self.campaign_file_path)
        get_ad_groups(self.ad_group_file_path)
        get_search_terms(self.search_term_file_path)

        grouped_by_ad_group = df.groupby(["ad_group_id", "search_term"],
                                         as_index=False).sum()
        grouped_by_ad_group["roas"] = grouped_by_ad_group. \
            apply(
            lambda row:
            row["conversion_value"] / row["cost"]
            if row["cost"] else 0,
            axis=1
        )
        grouped_by_ad_group = grouped_by_ad_group. \
            sort_values("roas", ascending=False)

        sorted_alias_roases = [
            float(x) for x in
            SearchTerm.objects.
            get_top_searches('ad_group__alias').
            values_list('roas', flat=True)
        ]
        for i in zip(sorted_alias_roases,
                     grouped_by_ad_group.roas.to_list()[:10]):
            self.assertTrue(math.isclose(*i, abs_tol=.00001))

        sorted_alias_search_terms = SearchTerm.objects. \
            get_top_searches('ad_group__alias'). \
            values_list('search_term', flat=True)

        self.assertListEqual(list(sorted_alias_search_terms),
                             grouped_by_ad_group.search_term.to_list()[:10])

        grouped_by_campaign = df.groupby(["campaign_id", "search_term"],
                                         as_index=False).sum()
        grouped_by_campaign["roas"] = grouped_by_campaign. \
            apply(
                lambda row:
                row["conversion_value"] / row["cost"]
                if row["cost"] else 0,
                axis=1
        )
        grouped_by_campaign = grouped_by_campaign. \
            sort_values("roas", ascending=False)

        sorted_campaign_roases = [
            float(x) for x in
            SearchTerm.objects.
            get_top_searches('campaign__structure_value').
            values_list('roas', flat=True)
        ]

        for i in zip(sorted_campaign_roases,
                     grouped_by_campaign.roas.to_list()[:10]):
            self.assertTrue(math.isclose(*i, abs_tol=.001))

        sorted_campaign_search_terms = SearchTerm.objects. \
            get_top_searches('campaign__structure_value'). \
            values_list('search_term', flat=True)

        self.assertListEqual(list(sorted_campaign_search_terms),
                             grouped_by_campaign.search_term.to_list()[:10])
