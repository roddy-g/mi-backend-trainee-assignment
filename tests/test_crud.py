from api.crud import *
from datetime import datetime


def test_get_date_some_days_ago():
    assert get_date_some_days_ago(0).date() == datetime.today().date()