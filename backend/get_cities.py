'''
Get the cities that should be displayed in the application.

Functions:
    get_cities(min_temp, max_temp, month) -> list[str]
'''

from get_database import get_database


def get_cities(min_temp, max_temp, month):
    '''
    Returns all cities where the temperature is in between a provided range.

        Parameters:
            min_temp (str): A string representing the minimum temperature
            max_temp (str): A string representing the maximum temperature
            month (str): A string representing the month

        Returns:
            cities (list[str]): List of strings of the cities where the the temperature 
            for the month is greater than or equal to min_temp and less than or equal to max_temp
    '''

    dbname = get_database()
    cities_collection = dbname["cities"]

    cities = list(cities_collection.find({
        f"months.{month}.temperature": {
            "$lte": float(max_temp),
            "$gte": float(min_temp)
        }
    }, {
        '_id': 0,
        'city': 1,
        'country': 1,
        f"months.{month}.temperature": 1
    }))

    return cities
