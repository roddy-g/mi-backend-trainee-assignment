from api.schemas import AdvertStats
from datetime import datetime


test_advert_stats = AdvertStats(phrase='test register',
                                location_id=637640,
                                advert_count=100,
                                timestamp=datetime.now())
