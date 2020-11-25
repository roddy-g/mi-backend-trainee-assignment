import schemas
import requests
from datetime import datetime


def get_data_stat(advertise: schemas.Advert):
    url = 'https://m.avito.ru/api/10/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&query={}&locationId={}'\
        .format(advertise.phrase, advertise.location_id)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        advert_count = data['result']['totalCount']
        timestamp = datetime.now()
        advert_stats = schemas.AdvertStats(phrase=advert.phrase,
                                           location_id=advert.location_id,
                                           advert_count=advert_count,
                                           timestamp=timestamp)
        return advert_stats


if __name__ == "__main__":
    advert = schemas.Advert(phrase='iphone', location_id=637640)
    result = get_data_stat(advert)
    print(result)



