from api.schemas import ItemStats
from datetime import datetime

timestamp = datetime.now()
test_item_stats_count_30 = ItemStats(phrase='test register',
                                     location_id=637640,
                                     advert_count=30,
                                     timestamp=timestamp)

test_item_stats_count_70 = ItemStats(phrase='test register',
                                     location_id=637640,
                                     advert_count=70,
                                     timestamp=timestamp)

test_item_stats_count_170 = ItemStats(phrase='test register',
                                      location_id=637640,
                                      advert_count=170,
                                      timestamp=timestamp)

item_stats = [test_item_stats_count_30, test_item_stats_count_70, test_item_stats_count_170]