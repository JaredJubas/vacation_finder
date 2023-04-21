'''
A module for adding city temperature data to a MongoDB database.

Functions:
    convert_temp_to_float(temp_string: str) -> float
        Converts a temperature string to a float in Celsius.

    fetch_city_data() -> pd.DataFrame
        Fetches city temperature data from a Wikipedia page and returns it as a Pandas DataFrame.

    build_city_dict(row: pd.Series) -> Dict[str, Any]
        Builds a dictionary representing a city's data in the format expected by the database.

    add_temperature_to_db() -> None
        Adds city temperature data to the database.

Example usage:
    # Should be called through update-data script
    # Call from command line to update temperature data:
    # yarn update-data --temperature

Notes:
    This module requires the get_database module to be imported.
    The Wikipedia page used to fetch the data is hardcoded as WIKI_URL.
    MONTH_NAMES is a list of month names used to extract temperature data from the DataFrame.
    The database collection name is hardcoded as "cities".
'''

from typing import Dict, Any
import sys
sys.path.insert(0, '..') # Add parent directory to sys.path

from get_database import get_database
import pandas as pd

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_cities_by_average_temperature"
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May",
               "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def convert_temp_to_float(temp_string: str) -> float:
    '''
    Returns the temperature as a float in celsius.

        Parameters:
            temp_string (str): A string representing the temperature. The string has the format 
            °C (°F).

        Returns:
            temperature (float): The temperature as a float in celsius.
    '''

    try:
        celsius = temp_string.split(' ')[0].replace("−", "-")
        return float(celsius)
    except (ValueError, AttributeError):
        return float("nan")


def fetch_city_data() -> pd.DataFrame:
    '''
    Fetches city temperature data from the Wikipedia page and returns it as a Pandas DataFrame.

        Parameters:
            None

        Returns:
            city_data (DataFrame): The Pandas DataFrame of the Wikipedia page.
    '''

    return pd.read_html(WIKI_URL)[0]


def build_city_dict(row: pd.Series) -> Dict[str, Any]:
    '''
    Takes a row from the city data DataFrame and returns a dictionary representing the city's data 
    in the format expected by the database.

        Parameters:
            row (Series): A row from the city data DataFrame.

        Returns:
            city_dict (Dict[str, Any]): The city's data in the following format:
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
    '''

    city = row['City']
    country = row['Country']
    months = {}

    for month_name in MONTH_NAMES:
        month_data = {"temperature": convert_temp_to_float(row[month_name])}
        months[month_name.lower()[:3]] = month_data

    return {"city": city, "country": country, "months": months}


def add_temperature_to_db():
    '''
    Adds city temperature data to the database.

        Parameters:
            None

        Returns:
            None
    '''

    dbname = get_database()
    cities_collection = dbname["cities"]

    city_data = fetch_city_data()

    for _, row in city_data.iterrows():
        city_dict = build_city_dict(row)

        cities_collection.update_one(
            {"city": city_dict["city"], "country": city_dict["country"]},
            {"$set": city_dict},
            upsert=True,
        )
