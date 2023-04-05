'''
Get the cities that should be displayed in the application.

Functions:
    get_cities(min_temp, max_temp, month) -> list[str]
'''


def get_cities(min_temp, max_temp, month, dbname):
    '''
    Returns all cities where the temperature is in between a provided range.

        Preconditions:
            min_temp: str with value <= max_temp
            max_temp: str with value >= max_temp
            month: str with value in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 
                                      'sep', 'oct', 'nov', 'dec']

        Parameters:
            min_temp (str): A string representing the minimum temperature
            max_temp (str): A string representing the maximum temperature
            month (str): A string representing the month

        Returns:
            cities (dict[list[dict[str: str, str: float]]]): All cities where the min_temp is less 
            than or equal to the max_temp for the provided month. The return should be a dictionary 
            where the key is a country and the value is a list that contains all cities in this 
            country that satisfy the above condition. This list would contain a dictionary of the 
            city and the temperature for the provided month.

    '''
    valid_months = ['jan', 'feb', 'mar', 'apr', 'may',
                    'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    assert month in valid_months

    assert min_temp <= max_temp

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

    cities_grouped = {}

    for city_dict in cities:
        country = city_dict['country']
        city_to_insert = {
            'city': city_dict['city'], 'temperature': city_dict['months'][month]['temperature']
        }
        if country in cities_grouped:
            cities_grouped[country].append(city_to_insert)
        else:
            cities_grouped[country] = [city_to_insert]

    return cities_grouped
