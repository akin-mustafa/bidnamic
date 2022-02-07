import pandas as pd
from django.conf import settings
from django.test import TestCase

from bidnamic.ad_groups.models import AdGroup
from bidnamic.ad_groups.tasks import get_ad_groups
from bidnamic.campaigns.tasks import get_campaigns


class TaskTestCase(TestCase):
    def setUp(self) -> None:
        app_dir = settings.APPS_DIR / "utils/tests/data_files"
        self.campaign_file_path = app_dir / "campaigns.csv"
        self.ad_group_file_path = app_dir / "adgroups.csv"

    def test_get_ad_groups(self):
        get_ad_groups(self.ad_group_file_path)
        ad_group_df = pd.read_csv(self.ad_group_file_path).drop_duplicates()
        campaign_df = pd.read_csv(self.campaign_file_path).drop_duplicates()

        self.assertEqual(0, AdGroup.objects.count())
        get_campaigns(self.campaign_file_path)
        get_ad_groups(self.ad_group_file_path)
        ad_group_df = ad_group_df[ad_group_df.campaign_id.isin(campaign_df.campaign_id)]
        self.assertListEqual(
            list(
                AdGroup.objects.all()
                .distinct("id")
                .values_list("id", flat=True)
                .order_by("id")
            ),
            sorted(ad_group_df.ad_group_id.to_list()),
        )
        self.assertListEqual(
            sorted(
                ad_group_df.drop_duplicates(
                    subset=["campaign_id"]
                ).campaign_id.to_list()
            ),
            list(
                AdGroup.objects.all()
                .distinct("campaign_id")
                .values_list("campaign_id", flat=True)
                .order_by("campaign_id")
            ),
        )
