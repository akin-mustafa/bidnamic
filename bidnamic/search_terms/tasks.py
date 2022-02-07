import logging

from rest_framework.exceptions import ValidationError

from bidnamic.search_terms.models import SearchTerm
from bidnamic.search_terms.serializers import SearchTermSerializer
from bidnamic.utils import read_csv_file, get_not_recorded_data, \
    exclude_non_existing_campaigns
from config import celery_app

logger = logging.getLogger()

SEARCH_TERM_URL: str = 'https://raw.githubusercontent.com/bidnamic/' \
                    'bidnamic-python-challenge/master/search_terms.csv'
CHUNK_SIZE: int = 10000


@celery_app.task()
def get_search_terms():
    for chunk in read_csv_file(SEARCH_TERM_URL, CHUNK_SIZE):
        chunk = exclude_non_existing_campaigns(
            get_not_recorded_data(
                SearchTerm, chunk, 'ad_group_id', 'ad_group_id'
            )
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