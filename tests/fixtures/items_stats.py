from api.schemas import ItemStats
from datetime import datetime

timestamp = datetime.now()
test_item_stats_count_30 = ItemStats(item_id=1,
                                     items_quantity=30,
                                     timestamp=timestamp)

test_item_stats_count_70 = ItemStats(item_id=1,
                                     items_quantity=70,
                                     timestamp=timestamp)

test_item_stats_count_170 = ItemStats(item_id=1,
                                      items_quantity=170,
                                      timestamp=timestamp)

item_stats = [test_item_stats_count_30, test_item_stats_count_70, test_item_stats_count_170]