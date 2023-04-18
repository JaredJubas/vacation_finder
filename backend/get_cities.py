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
            month: str with value that is a valid month of the year

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

    assert month in valid_months

    float_min_temp = float(min_temp)
    float_max_temp = float(max_temp)

    assert float_min_temp <= float_max_temp

    shortened_month = month[:3].lower()

    cities_collection = dbname["cities"]

    cities = list(cities_collection.find({
        f"months.{shortened_month}.temperature": {
            "$lte": float_max_temp,
            "$gte": float_min_temp
        }
    }, {
        '_id': 0,
        'city': 1,
        'country': 1,
        f"months.{shortened_month}.temperature": 1
    }))

    cities_grouped = {}

    for city_dict in cities:
        country = city_dict['country']
        city_to_insert = {
            'city': city_dict['city'], 'temperature': city_dict['months'][shortened_month]['temperature']
        }
        if country in cities_grouped:
            cities_grouped[country].append(city_to_insert)
        else:
            cities_grouped[country] = [city_to_insert]

    return cities_grouped
