'''
Test functions for the gte_cities function
'''
# TODO move testing to own folder in root

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
    }
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
    }
}

database["cities"].insert_many([toronto, ottawa])


def test_invalid_temp():
    min_temp = '1'
    max_temp = '0'
    month = 'January'

    with pytest.raises(AssertionError):
        get_cities(min_temp, max_temp, month, database)


def test_invalid_month():
    min_temp = '1'
    max_temp = '5'
    month = 'Januaryv'

    with pytest.raises(AssertionError):
        get_cities(min_temp, max_temp, month, database)


def test_invalid_month_casing():
    min_temp = '1'
    max_temp = '5'
    month = 'january'

    with pytest.raises(AssertionError):
        get_cities(min_temp, max_temp, month, database)


def test_no_cities_valid():
    min_temp = '1'
    max_temp = '5'
    month = 'February'

    cities = get_cities(min_temp, max_temp, month, database)

    assert not cities


def test_some_cities_valid():
    min_temp = '10'
    max_temp = '12'
    month = 'May'

    cities = get_cities(min_temp, max_temp, month, database)

    assert cities == {'Canada': [{'city': 'Toronto', 'temperature': 10}]}


def test_all_cities_valid():
    min_temp = '20'
    max_temp = '23'
    month = 'August'

    cities = get_cities(min_temp, max_temp, month, database)

    assert cities == {'Canada': [{'city': 'Toronto', 'temperature': 20.1}, {
        'city': 'Ottawa', 'temperature': 23}]}
