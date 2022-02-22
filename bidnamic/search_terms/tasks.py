import logging
from pathlib import Path
from typing import Union

from pandas import DataFrame
from rest_framework.exceptions import ValidationError

from bidnamic.ad_groups.tasks import get_ad_groups
from bidnamic.campaigns.tasks import get_campaigns
from bidnamic.search_terms.models import SearchTerm
from bidnamic.search_terms.serializers import SearchTermSerializer
from bidnamic.utils.helpers import (
    exclude_non_existing_campaigns,
    get_not_recorded_data,
    read_csv_file,
)
from config import celery_app

logger = logging.getLogger()

SEARCH_TERM_URL: str = (
    "https://raw.githubusercontent.com/bidnamic/"
    "bidnamic-python-challenge/master/search_terms.csv"
)


@celery_app.task()
def get_search_terms(path: Union[str, Path, None] = None,
                     chunk_size: int = 2000):
    path = path or SEARCH_TERM_URL
    for chunk in read_csv_file(path, chunk_size):
        create_search_terms(chunk)


def create_search_terms(chunk: DataFrame):
    chunk = exclude_non_existing_campaigns(
        get_not_recorded_data(SearchTerm, chunk, "ad_group_id", "ad_group_id")
    )
    search_term_objects = []
    for search_term in chunk.itertuples():
        data = dict(
            date=search_term.date,
            ad_group=search_term.ad_group_id,
            campaign=search_term.campaign_id,
            clicks=search_term.clicks,
            cost=search_term.cost,
            conversion_value=search_term.conversion_value,
            conversions=search_term.conversions,
            search_term=search_term.search_term,
        )
        try:
            serializer = SearchTermSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            search_term_objects.append(SearchTerm(**serializer.validated_data))
        except ValidationError as e:
            logger.warning(e)
    SearchTerm.objects.bulk_create(search_term_objects)


@celery_app.task()
def get_all(chunk_size: int = 2000):
    get_campaigns(chunk_size=chunk_size)
    get_ad_groups(chunk_size=chunk_size)
    get_search_terms(chunk_size=chunk_size)
