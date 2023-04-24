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
        "jan": {"temperature": -5.2},
        "feb": {"temperature": -2.9},
        "mar": {"temperature": 1.8},
        "apr": {"temperature": 4.7},
        "may": {"temperature": 10},
        "jun": {"temperature": 19.5},
        "jul": {"temperature": 22.6},
        "aug": {"temperature": 20.1},
        "sep": {"temperature": 15.4},
        "oct": {"temperature": 9.8},
        "nov": {"temperature": 7.6},
        "dec": {"temperature": 2.1}
    },
    "safety": 1
}

ottawa = {
    "city": "Ottawa",
    "country": "Canada",
    "months": {
        "jan": {"temperature": -7.2},
            "feb": {"temperature": -2.9},
            "mar": {"temperature": 1.8},
            "apr": {"temperature": 4.7},
            "may": {"temperature": 12.1},
            "jun": {"temperature": 19.5},
            "jul": {"temperature": 22.6},
            "aug": {"temperature": 23},
            "sep": {"temperature": 15.4},
            "oct": {"temperature": 9.8},
            "nov": {"temperature": 7.6},
            "dec": {"temperature": 2.1}
    },
    "safety": 1
}

mexico_city = {
    "city": "Mexico City",
    "country": "Mexico",
    "months": {
        "jan": {"temperature": 27.2},
        "feb": {"temperature": 22.9},
        "mar": {"temperature": 21.8},
        "apr": {"temperature": 24.7},
        "may": {"temperature": 22.1},
        "jun": {"temperature": 29.5},
        "jul": {"temperature": 22.6},
        "aug": {"temperature": 25},
        "sep": {"temperature": 25.4},
        "oct": {"temperature": 29.8},
        "nov": {"temperature": 27.6},
        "dec": {"temperature": 22.9}
    },
    "safety": 2
}

kabul = {
    "city": "Kabul",
    "country": "Afghanistan",
    "months": {
        "jan": {"temperature": 27.2},
        "feb": {"temperature": 22.9},
        "mar": {"temperature": 21.8},
        "apr": {"temperature": 24.7},
        "may": {"temperature": 22.1},
        "jun": {"temperature": 29.5},
        "jul": {"temperature": 22.6},
        "aug": {"temperature": 25},
        "sep": {"temperature": 25.4},
        "oct": {"temperature": 29.8},
        "nov": {"temperature": 27.6},
        "dec": {"temperature": 22.9}
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

    with pytest.raises(ValueError):
        get_cities(min_temp, max_temp, month, database)


def test_invalid_month():
    '''
    Tests that a ValueError is thrown if the month is not a valid month of the year.
    '''

    min_temp = '1'
    max_temp = '5'
    month = 'Januaryv'

    with pytest.raises(ValueError):
        get_cities(min_temp, max_temp, month, database)


def test_invalid_month_casing():
    '''
    Tests that a ValueError is thrown if the month is a valid month, but does not start with a
    capital letter.
    '''

    min_temp = '1'
    max_temp = '5'
    month = 'january'

    with pytest.raises(ValueError):
        get_cities(min_temp, max_temp, month, database)


def test_no_cities_valid():
    '''
    Tests that an empty dictionary is returned if there are no cities where the temperature is 
    between min_temp and max_temp for a given month.
    '''

    min_temp = '1'
    max_temp = '5'
    month = 'February'

    cities = get_cities(min_temp, max_temp, month, database)

    assert not cities


def test_one_city_valid():
    '''
    Tests that a single city gets returned if multiple cities exist in the database, but only one
    city has the temperature between min_temp and max_temp for a given month.
    '''

    min_temp = '10'
    max_temp = '12'
    month = 'May'

    cities = get_cities(min_temp, max_temp, month, database)

    assert cities == {'Canada': [{'city': 'Toronto', 'temperature': 10}]}


def test_multiple_cities_valid():
    '''
    Tests that multiple cities get returned, grouped under the same country, if multiple cities
    exist in the database where the temperature for a given month is between min_temp and max_temp
    and the cities are in the same country.
    '''

    min_temp = '20'
    max_temp = '23'
    month = 'August'

    cities = get_cities(min_temp, max_temp, month, database)

    assert cities == {'Canada': [{'city': 'Toronto', 'temperature': 20.1}, {
        'city': 'Ottawa', 'temperature': 23}]}


def test_multiple_countries_valid():
    '''
    Tests that multiple cities get returned, grouped by country, if multiple cities exist in the 
    database where the temperature for a given month is between min_temp and max_temp and the cities
    are in more than one country.
    '''

    min_temp = '20'
    max_temp = '25'
    month = 'August'

    cities = get_cities(min_temp, max_temp, month, database)

    assert cities == {
        'Canada': [{'city': 'Toronto', 'temperature': 20.1}, {'city': 'Ottawa', 'temperature': 23}],
        'Mexico': [{'city': 'Mexico City', 'temperature': 25}]}
