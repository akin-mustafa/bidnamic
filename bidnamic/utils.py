from typing import Generator, TypeVar, Type

import pandas as pd
from django.db.models import Model
from pandas import DataFrame

from bidnamic.campaigns.models import Campaign

T = TypeVar('T', bound=Model)


def read_csv_file(path: str,
                  chunk_size: int) -> Generator[DataFrame, None, None]:
    for chunk in pd.read_csv(path, chunksize=chunk_size):
        yield chunk


def get_not_recorded_data(model: Type[T],
                          chunk: DataFrame,
                          field: str,
                          model_field: str = 'pk',
                          ) -> DataFrame:
    chunk.drop_duplicates(inplace=True)
    data_ids_list = getattr(chunk, field).to_list()
    existing_ids = model.objects. \
        filter(**{f'{model_field}__in': data_ids_list}). \
        values_list('pk', flat=True)
    non_exists_ids = list(set(data_ids_list) - set(existing_ids))
    chunk = chunk[getattr(chunk, field).isin(non_exists_ids)]
    return chunk


def exclude_non_existing_campaigns(chunk: DataFrame) -> DataFrame:
    campaign_ids_list = chunk.campaign_id.to_list()
    existing_campaign_ids_list = Campaign.objects. \
        filter(pk__in=campaign_ids_list). \
        values_list('pk', flat=True)
    chunk = chunk[chunk.campaign_id.isin(existing_campaign_ids_list)]
    return chunk
