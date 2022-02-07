from math import ceil

import pandas
from django.conf import settings
from django.test import TestCase

from bidnamic.ad_groups.models import AdGroup
from bidnamic.ad_groups.tasks import create_ad_groups
from bidnamic.campaigns.tasks import get_campaigns
from bidnamic.utils.helpers import get_not_recorded_data, read_csv_file


class HelperTestCase(TestCase):
    def setUp(self) -> None:
        app_dir = settings.APPS_DIR / "utils/tests/data_files"
        self.campaign_file_path = app_dir / "campaigns.csv"
        self.ad_group_file_path = app_dir / "adgroups.csv"
        self.search_term_file_path = app_dir / "search_terms.csv"

    def test_read_csv_file(self):
        chunks = read_csv_file(self.campaign_file_path, 23)
        df = pandas.read_csv(self.campaign_file_path)

        self.assertEqual(len(list(chunks)), ceil(len(df.index) / 23))

        chunks = read_csv_file(self.campaign_file_path, 10)
        self.assertEqual(len(list(chunks)), ceil(len(df.index) / 10))

    def test_get_not_recorded_data(self):
        get_campaigns(self.campaign_file_path)

        df = pandas.read_csv(self.ad_group_file_path, chunksize=10).get_chunk()
        create_ad_groups(df)
        ad_group_df = pandas.read_csv(self.ad_group_file_path).drop_duplicates()

        compare_df = get_not_recorded_data(AdGroup, ad_group_df, "ad_group_id")
        ad_group_df = ad_group_df[~ad_group_df.ad_group_id.isin(df.ad_group_id)]

        self.assertListEqual(
            compare_df.ad_group_id.to_list(), ad_group_df.ad_group_id.to_list()
        )
