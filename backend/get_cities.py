"""
This module defines a function to retrieve cities based on temperature and rainy days criteria from
a database.

Functions:
    get_cities(min_temp: str, max_temp: str, month: str, rainy_days: str, dbname: Database) -> dict
        Retrieves all cities where the temperature is within a specified range and the average
        number of rainy days is less than or equal to a provided value.
"""

from collections import defaultdict

from mongomock import Database

def get_cities(min_temp: str, max_temp: str, month: str, rainy_days: str, dbname: Database) -> dict:
    '''
    Returns all cities where the temperature is in between a provided range.

        Preconditions:
            min_temp: str with value <= max_temp
            max_temp: str with value >= max_temp
            month: str with value that is a valid month of the year, starting with a capital letter

        Parameters:
            min_temp (str): A string representing the minimum temperature
            max_temp (str): A string representing the maximum temperature
            month (str): A string representing the month (e.g., 'January', 'February', etc.)
            rainy_days (str): A string representing the maximum number of rainy days
            dbname (Database): The name of the database to be used

        Returns:
            cities (dict[list[dict[str: str, str: float]]]): All cities where the min_temp is less 
            than or equal to the max_temp for the provided month an the average number of rainy days
            is less than or equal to rainy_days. The return should be a dictionary where the key is
            a country and the value is a list that contains all cities in this country that satisfy
            the above condition. This list would contain a dictionary of the city and the
            temperature for the provided month.

    '''
    valid_months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
    ]

    if month not in valid_months:
        raise ValueError(
            f"Invalid month: {month}. Please provide a valid month.")

    try:
        float_min_temp = float(min_temp)
        float_max_temp = float(max_temp)
    except ValueError as exc:
        raise ValueError("Invalid temperature values. Please provide numbers.") from exc

    if float_min_temp > float_max_temp:
        raise ValueError(
            "Minimum temperature cannot be greater than maximum temperature.")

    float_rainy_days = float(rainy_days)
    shortened_month = month[:3].lower()

    cities_collection = dbname["cities"]

    # The values for safety in the database has the following meaning:
    # 'Take normal security precautions': 1,
    # 'Exercise a high degree of caution': 2,
    # 'Avoid non-essential travel': 3,
    # 'Avoid all travel': 4
    # We want safe countries so safety value should be 1 or 2
    cities = list(cities_collection.find({
        f"months.{shortened_month}.temperature": {
            "$lte": float_max_temp,
            "$gte": float_min_temp
        },
        f"months.{shortened_month}.rain": {
            "$lte": float_rainy_days
        },
        "safety": {"$in": [1, 2]}
    }, {
        '_id': 0,
        'city': 1,
        'country': 1,
        f"months.{shortened_month}": 1
    }))

    cities_by_country = defaultdict(list)

    for city in cities:
        country = city['country']
        city_data = {
            'city': city['city'],
            'temperature': city['months'][shortened_month]['temperature'],
            'rain': city['months'][shortened_month]['rain']
        }
        cities_by_country[country].append(city_data)

    return dict(cities_by_country)
