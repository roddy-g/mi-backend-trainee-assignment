from api import get_data_from_avito, schemas

def test_get_data_from_avito():
    moscow_location_id = 637640
    phrase = 'iphone'
    advert = schemas.Advert(phrase=phrase, location_id=moscow_location_id)
    assert get_data_from_avito.get_data_stat(advert) is not None
    assert get_data_from_avito.get_data_stat(advert) != 'Not 200 status code'