'''
Test cases for the get_cities function
'''

import pytest
import mongomock

from get_cities import get_cities


database = mongomock.MongoClient().db

toronto = {
    "city": "Toronto",
    "country": "Canada",
    "months": {
        "jan": {"temperature": -5.2, "rain": 4.2},
        "feb": {"temperature": -2.9, "rain": 5.1},
        "mar": {"temperature": 1.8, "rain": 4.6},
        "apr": {"temperature": 4.7, "rain": 7.6},
        "may": {"temperature": 10, "rain": 6.6},
        "jun": {"temperature": 19.5, "rain": 4},
        "jul": {"temperature": 22.6, "rain": 3.1},
        "aug": {"temperature": 20.1, "rain": 2.3},
        "sep": {"temperature": 15.4, "rain": 5.6},
        "oct": {"temperature": 9.8, "rain": 0.8},
        "nov": {"temperature": 7.6, "rain": 1},
        "dec": {"temperature": 2.1, "rain": 22}
    },
    "safety": 1
}

ottawa = {
    "city": "Ottawa",
    "country": "Canada",
    "months": {
        "jan": {"temperature": -7.2, "rain": 5.6},
            "feb": {"temperature": -2.9, "rain": 3.4},
            "mar": {"temperature": 1.8, "rain": 1},
            "apr": {"temperature": 4.7, "rain": 2.3},
            "may": {"temperature": 12.1, "rain": 2.6},
            "jun": {"temperature": 19.5, "rain": 3.4},
            "jul": {"temperature": 22.6, "rain": 4.54},
            "aug": {"temperature": 23, "rain": 6.56},
            "sep": {"temperature": 15.4, "rain": 8.97},
            "oct": {"temperature": 9.8, "rain": 5.56},
            "nov": {"temperature": 7.6, "rain": 19},
            "dec": {"temperature": 2.1, "rain": 2.3}
    },
    "safety": 1
}

mexico_city = {
    "city": "Mexico City",
    "country": "Mexico",
    "months": {
        "jan": {"temperature": 27.2, "rain": 0.01},
        "feb": {"temperature": 22.9, "rain": 0.4},
        "mar": {"temperature": 21.8, "rain": 0.6},
        "apr": {"temperature": 24.7, "rain": 0.7},
        "may": {"temperature": 22.1, "rain": 0.8},
        "jun": {"temperature": 29.5, "rain": 1.3},
        "jul": {"temperature": 22.6, "rain": 1.2},
        "aug": {"temperature": 25, "rain": 1.6},
        "sep": {"temperature": 25.4, "rain": 11.4},
        "oct": {"temperature": 29.8, "rain": 3.4},
        "nov": {"temperature": 27.6, "rain": 15.4},
        "dec": {"temperature": 22.9, "rain": 4.5}
    },
    "safety": 2
}

kabul = {
    "city": "Kabul",
    "country": "Afghanistan",
    "months": {
        "jan": {"temperature": 27.2, "rain": 1.1},
        "feb": {"temperature": 22.9, "rain": 1.1},
        "mar": {"temperature": 21.8, "rain": 1.2},
        "apr": {"temperature": 24.7, "rain": 1.6},
        "may": {"temperature": 22.1, "rain": 0.7},
        "jun": {"temperature": 29.5, "rain": 0.5},
        "jul": {"temperature": 22.6, "rain": 0.4},
        "aug": {"temperature": 25, "rain": 1},
        "sep": {"temperature": 25.4, "rain": 0.2},
        "oct": {"temperature": 29.8, "rain": 0.3},
        "nov": {"temperature": 27.6, "rain": 0.5},
        "dec": {"temperature": 22.9, "rain": 10.65}
    },
    "safety": 4
}

database["cities"].insert_many([toronto, ottawa, mexico_city, kabul])


def test_invalid_temperature_range():
    '''
    Tests that a ValueError is thrown if max_temp < min_temp.
    '''

    min_temp = '1'
    max_temp = '0'
    month = 'January'
    rainy_days = '2'

    with pytest.raises(ValueError):
        get_cities(min_temp, max_temp, month, rainy_days, database)


def test_invalid_month():
    '''
    Tests that a ValueError is thrown if the month is not a valid month of the year.
    '''

    min_temp = '1'
    max_temp = '5'
    month = 'Januaryv'
    rainy_days = '2'

    with pytest.raises(ValueError):
        get_cities(min_temp, max_temp, month, rainy_days, database)


def test_invalid_month_casing():
    '''
    Tests that a ValueError is thrown if the month is a valid month, but does not start with a
    capital letter.
    '''

    min_temp = '1'
    max_temp = '5'
    month = 'january'
    rainy_days = '2'

    with pytest.raises(ValueError):
        get_cities(min_temp, max_temp, month, rainy_days, database)


def test_no_cities_valid():
    '''
    Tests that an empty dictionary is returned if there are no cities where the temperature is 
    between min_temp and max_temp for a given month.
    '''

    min_temp = '1'
    max_temp = '5'
    month = 'February'
    rainy_days = '2'

    cities = get_cities(min_temp, max_temp, month, rainy_days, database)

    assert not cities


def test_one_city_valid():
    '''
    Tests that a single city gets returned if multiple cities exist in the database, but only one
    city has the temperature between min_temp and max_temp for a given month.
    '''

    min_temp = '10'
    max_temp = '12'
    month = 'May'
    rainy_days = '8'

    cities = get_cities(min_temp, max_temp, month, rainy_days, database)

    assert cities == {'Canada': [{'city': 'Toronto', 'temperature': 10, 'rain': 6.6}]}


def test_multiple_cities_valid():
    '''
    Tests that multiple cities get returned, grouped under the same country, if multiple cities
    exist in the database where the temperature for a given month is between min_temp and max_temp
    and the cities are in the same country.
    '''

    min_temp = '20'
    max_temp = '23'
    month = 'August'
    rainy_days = '8'

    cities = get_cities(min_temp, max_temp, month, rainy_days, database)

    assert cities == {
        'Canada': [{'city': 'Toronto', 'temperature': 20.1, 'rain': 2.3}, 
                   {'city': 'Ottawa', 'temperature': 23, 'rain': 6.56}]
        }
    
def test_multiple_valid_temp_one_valid_rain():
    '''
    Tests that multiple cities get returned, grouped under the same country, if multiple cities
    exist in the database where the temperature for a given month is between min_temp and max_temp
    and the cities are in the same country.
    '''

    min_temp = '20'
    max_temp = '23'
    month = 'August'
    rainy_days = '6'

    cities = get_cities(min_temp, max_temp, month, rainy_days, database)

    assert cities == {
        'Canada': [{'city': 'Toronto', 'temperature': 20.1, 'rain': 2.3}]
    }


def test_multiple_countries_valid():
    '''
    Tests that multiple cities get returned, grouped by country, if multiple cities exist in the 
    database where the temperature for a given month is between min_temp and max_temp and the cities
    are in more than one country.
    '''

    min_temp = '20'
    max_temp = '25'
    month = 'August'
    rainy_days = '8'

    cities = get_cities(min_temp, max_temp, month, rainy_days, database)

    assert cities == {
        'Canada': [{'city': 'Toronto', 'temperature': 20.1, 'rain': 2.3}, 
                   {'city': 'Ottawa', 'temperature': 23, 'rain': 6.56}],
        'Mexico': [{'city': 'Mexico City', 'temperature': 25, 'rain': 1.6}]
        }
