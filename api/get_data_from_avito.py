from api import schemas
import requests
from datetime import datetime


def get_data_stat(advertise: schemas.Advert):
    url = 'https://m.avito.ru/api/10/' \
          'items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&' \
          'query={}&locationId={}'\
        .format(advertise.phrase, advertise.location_id)
    response = requests.get(url)
    data = response.json()
    try:
        advert_count = data['result']['totalCount']
        timestamp = datetime.now()
        advert_stats = schemas.AdvertStats(phrase=advertise.phrase,
                                           location_id=advertise.location_id,
                                           advert_count=advert_count,
                                           timestamp=timestamp)
        return advert_stats
    except KeyError:
        return None
