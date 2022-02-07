import logging

from rest_framework.exceptions import ValidationError

from bidnamic.campaigns.models import Campaign
from bidnamic.campaigns.serializers import CampaignSerializer
from bidnamic.utils import read_csv_file, get_not_recorded_data
from config import celery_app

logger = logging.getLogger()

CAMPAIGN_URL: str = 'https://raw.githubusercontent.com/bidnamic/' \
                    'bidnamic-python-challenge/master/campaigns.csv'
CHUNK_SIZE: int = 10000


@celery_app.task()
def get_campaigns():
    for chunk in read_csv_file(CAMPAIGN_URL, CHUNK_SIZE):
        chunk = get_not_recorded_data(Campaign, chunk, 'campaign_id')
        campaign_objects = []
        for campaign in chunk.itertuples():
            data = dict(
                id=campaign.campaign_id,
                structure_value=campaign.structure_value,
                status=campaign.status,
            )
            try:
                serializer = CampaignSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                campaign_objects.append(Campaign(**serializer.validated_data))
            except ValidationError as e:
                logger.warning(e)

        Campaign.objects.bulk_create(campaign_objects)



