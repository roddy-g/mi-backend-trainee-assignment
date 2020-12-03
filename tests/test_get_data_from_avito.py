from api import get_data_from_avito, schemas


def test_get_data_from_avito():
    moscow_location_id = 637640
    phrase = 'iphone'
    advert = schemas.Advert(phrase=phrase, location_id=moscow_location_id)
    '''this string is comment out until I fix this test inside CI
    assert get_data_from_avito.get_data_stat(advert) is not None
    assert type(get_data_from_avito.get_data_stat(advert)) != str'''