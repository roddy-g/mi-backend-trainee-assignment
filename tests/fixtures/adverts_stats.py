from api.schemas import AdvertStats
from datetime import datetime

timestamp = datetime.now()
test_advert_stats_count_30 = AdvertStats(phrase='test register',
                                         location_id=637640,
                                         advert_count=30,
                                         timestamp=timestamp)

test_advert_stats_count_70 = AdvertStats(phrase='test register',
                                         location_id=637640,
                                         advert_count=70,
                                         timestamp=timestamp)

test_advert_stats_count_170 = AdvertStats(phrase='test register',
                                          location_id=637640,
                                          advert_count=170,
                                          timestamp=timestamp)

stats = [test_advert_stats_count_30, test_advert_stats_count_70, test_advert_stats_count_170]