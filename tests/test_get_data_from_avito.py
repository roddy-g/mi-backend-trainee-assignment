from api import get_data_from_avito, schemas

def test_get_data_from_avito():
    moscow_location_id = 637640
    advert = schemas.Advert(phrase='iphone', location_id=moscow_location_id)
    assert get_data_from_avito.get_data_stat(advert) is not None
