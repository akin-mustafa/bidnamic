import pandas as pd
from django.conf import settings
from django.test import TestCase

from bidnamic.campaigns.models import Campaign
from bidnamic.campaigns.tasks import get_campaigns


class TaskTestCase(TestCase):
    def setUp(self) -> None:
        app_dir = settings.APPS_DIR / "utils/tests/data_files"
        self.campaign_file_path = app_dir / "campaigns.csv"

    def test_get_ad_groups(self):
        campaign_df = pd.read_csv(self.campaign_file_path).drop_duplicates()

        self.assertEqual(0, Campaign.objects.count())
        get_campaigns(self.campaign_file_path)

        self.assertListEqual(
            list(
                Campaign.objects.all()
                .distinct("id")
                .values_list("id", flat=True)
                .order_by("id")
            ),
            sorted(campaign_df.campaign_id.to_list()),
        )
