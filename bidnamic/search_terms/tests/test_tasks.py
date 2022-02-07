import pandas as pd
from django.conf import settings
from django.test import TestCase

from bidnamic.ad_groups.models import AdGroup
from bidnamic.ad_groups.tasks import get_ad_groups
from bidnamic.campaigns.tasks import get_campaigns
from bidnamic.search_terms.models import SearchTerm
from bidnamic.search_terms.tasks import get_search_terms


class TaskTestCase(TestCase):
    def setUp(self) -> None:
        app_dir = settings.APPS_DIR / "utils/tests/data_files"
        self.campaign_file_path = app_dir / "campaigns.csv"
        self.ad_group_file_path = app_dir / "adgroups.csv"
        self.search_term_file_path = app_dir / "search_terms.csv"

    def test_get_ad_groups(self):
        get_search_terms(self.search_term_file_path)
        search_term_df = pd.read_csv(self.search_term_file_path).drop_duplicates()
        ad_group_df = pd.read_csv(self.ad_group_file_path).drop_duplicates()
        campaign_df = pd.read_csv(self.campaign_file_path).drop_duplicates()

        self.assertEqual(0, SearchTerm.objects.count())

        get_ad_groups(self.ad_group_file_path)
        get_search_terms(self.search_term_file_path)

        self.assertEqual(0, AdGroup.objects.count())

        get_campaigns(self.campaign_file_path)
        get_ad_groups(self.ad_group_file_path)
        get_search_terms(self.search_term_file_path)

        self.assertEqual(len(search_term_df.index), SearchTerm.objects.all().count())

        self.assertListEqual(
            list(
                SearchTerm.objects.all()
                .distinct("ad_group_id")
                .values_list("ad_group_id", flat=True)
                .order_by("ad_group_id")
            ),
            sorted(ad_group_df.ad_group_id.to_list()),
        )
        self.assertListEqual(
            sorted(campaign_df.campaign_id.to_list()),
            list(
                SearchTerm.objects.all()
                .distinct("campaign_id")
                .values_list("campaign_id", flat=True)
                .order_by("campaign_id")
            ),
        )
