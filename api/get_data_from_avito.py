from api import schemas
import requests
from datetime import datetime
from api.database_functions import get_item
from api.db import SessionLocal
from tests.fixtures import items


def get_data_stat(item: schemas.Item = items.test_item ):



    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        try:
            advert_count = data['result']['totalCount']
            timestamp = datetime.now()
            advert_stats = schemas.ItemStats(ited_id=1,
                                             items_quantity=advert_count,
                                             timestamp=timestamp)
            return advert_stats
        except KeyError:
            return 'keyErrddor'