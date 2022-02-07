import logging

from rest_framework.exceptions import ValidationError

from bidnamic.ad_groups.models import AdGroup
from bidnamic.ad_groups.serializers import AdGroupSerializer
from bidnamic.utils import (
    exclude_non_existing_campaigns,
    get_not_recorded_data,
    read_csv_file,
)
from config import celery_app

logger = logging.getLogger()

AD_GROUP_URL: str = (
    "https://raw.githubusercontent.com/bidnamic/"
    "bidnamic-python-challenge/master/adgroups.csv"
)


@celery_app.task()
def get_ad_groups(chunk_size: int = 2000):
    for chunk in read_csv_file(AD_GROUP_URL, chunk_size):
        chunk = get_not_recorded_data(AdGroup, chunk, "ad_group_id")
        chunk = exclude_non_existing_campaigns(chunk)
        ad_group_objects = []

        for ad_group in chunk.itertuples():
            data = dict(
                id=ad_group.ad_group_id,
                campaign=ad_group.campaign_id,
                alias=ad_group.alias,
                status=ad_group.status,
            )
            try:
                serializer = AdGroupSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                ad_group_objects.append(AdGroup(**serializer.validated_data))
            except ValidationError as e:
                logger.warning(e)

        AdGroup.objects.bulk_create(ad_group_objects)
