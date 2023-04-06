'''
Add data for cities to the database.

Functions:
    convert_temp_to_float(temp_string) -> float
    add_data_to_db(dfs) -> None
'''

import pandas as pd

from get_database import get_database


def convert_temp_to_float(temp_string):
    '''
    Returns the temperature as a float in celsius.

        Parameters:
            temp_string (str): A string representing the temperature. The string has the format 
            °C (°F).


        Returns:
            temperature (float): The temperature as a float in celsius.
    '''

    celsius = temp_string.split(' ')[0]

    # The minus sign from Wikipedia doesn't convert properly to a float so remove it
    removed = "".join(char for char in celsius if ord(char) < 128)

    # Add back the minus if it was removed
    temperature = - \
        float(removed) if len(celsius) != len(removed) else float(removed)

    return temperature


def add_data_to_db(dfs):
    '''
    Add all city information to the database. The document added should have the format:
    {
        city: str
        country: str
        months: {
            "jan": {
                "temperature": float
            },
            <insert other months here>,
            "dec": {
                "temperature": float
            }
        }
    }

    All months should be the first 3 letters of the month in lowercase.

    Paramaters:
        dfs (list[Dataframe]): A list of all the data tables from the Wikipedia page. Each dataframe
        in the list consists of a table with the columns: Country, City, Jan, <other months>, Dec, 
        Year, Ref. Each table is sorted by contintent. It is possible for the same country to appear
        in more than 1 table. 
    '''

    dbname = get_database()
    cities_collection = dbname["cities"]

    # Iterate over every table in dfs
    for _, dataframe in enumerate(dfs):

        # Iterate over every row in the table
        for _, row in dataframe.iterrows():
            current_city = row['City']
            current_country = row['Country']

            # Need to get the temperature for each month and convert them to floats
            months = {
                "jan": {
                    "temperature": convert_temp_to_float(row['Jan'])
                },
                "feb": {
                    "temperature": convert_temp_to_float(row['Feb'])
                },
                "mar": {
                    "temperature": convert_temp_to_float(row['Mar'])
                },
                "apr": {
                    "temperature": convert_temp_to_float(row['Apr'])
                },
                "may": {
                    "temperature": convert_temp_to_float(row['May'])
                },
                "jun": {
                    "temperature": convert_temp_to_float(row['Jun'])
                },
                "jul": {
                    "temperature": convert_temp_to_float(row['Jul'])
                },
                "aug": {
                    "temperature": convert_temp_to_float(row['Aug'])
                },
                "sep": {
                    "temperature": convert_temp_to_float(row['Sep'])
                },
                "oct": {
                    "temperature": convert_temp_to_float(row['Oct'])
                },
                "nov": {
                    "temperature": convert_temp_to_float(row['Nov'])
                },
                "dec": {
                    "temperature": convert_temp_to_float(row['Dec'])
                }
            }

            city_data = {
                "city": current_city,
                "country": current_country,
                "months": months
            }

            cities_collection.update_one({
                'city': current_city,
                'country': current_country
            }, {
                "$set": city_data
            },
                upsert=True
            )


if __name__ == "__main__":
    WIKI_URL = \
        "https://en.wikipedia.org/wiki/List_of_cities_by_average_temperature"
    data = pd.read_html(WIKI_URL)

    add_data_to_db(data)
