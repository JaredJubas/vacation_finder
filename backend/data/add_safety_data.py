"""
This module provides functions to scrape an HTML table of travel advisories from the Government of 
Canada website, map the advisory text to an integer safety value, and update the safety values in a
MongoDB database.

Data is taken from https://travel.gc.ca/travelling/advisories

Functions:
    get_html_table_data(url: str, headers: List[str]) -> pd.DataFrame
        Scrapes an HTML table from the given URL and returns it as a pandas DataFrame

    update_city_safety(collection: Collection, country: str, safety: int) -> None
        Updates the safety advisory value for a given country in the database.

    add_safety_to_db() -> None
        Main function that updates the safety advisory values in the database.

Example usage:
    # Should be called through update-data script
    # Call from command line to update safety data:
    # yarn update-data --safety

Notes:
    This module requires the get_database module to be imported.
    The logging level is set to INFO to write to the console.
    Uses the BeautifulSoup and pandas libraries.
    The database collection name is hardcoded as "cities".
    This module requires an internet connection to scrape the travel advisory table from the 
    Government of Canada website.
"""

import logging
import sys
from typing import Collection, List
sys.path.insert(0, '..')  # Add parent directory to sys.path

import pandas as pd
from bs4 import BeautifulSoup
import requests
from get_database import get_database


def get_html_table_data(url: str, headers: List[str]) -> pd.DataFrame:
    '''
    Scrapes an HTML table from the given URL and returns it as a pandas DataFrame.

        Parameters:
            url (str): The URL to scrape.
            headers (List[str]): A list of strings representing the column headers of the table.

        Returns:
            table_data (DataFrame): A pandas DataFrame representing the table data.
    '''

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table_data = pd.read_html(
            str(soup.find("table", id="reportlist")),
            header=0,
            parse_dates=True
        )[0]
        table_data = table_data.iloc[:, 1:3]
        table_data.columns = headers
        return table_data
    except requests.exceptions.RequestException as error:
        logging.error("An error occurred while scraping the webpage: %s", error)
        return None


def update_city_safety(collection: Collection, country: str, safety: int):
    '''
    Updates the safety advisory value for a given country in the database.

        Parameters:
            collection (Collection): The pymongo Collection to update.
            country (str): The name of the country to update.
            safety (int): The safety advisory value to set for the country.

        Returns:
            None
    '''

    result = collection.update_many(
        {'country': country},
        {'$set': {'safety': safety}}
    )
    logging.info(
        "Updated %s cities for %s safety advisory", result.modified_count, country)


def add_safety_to_db():
    '''
    Main function that updates the safety advisory values in the database.

        Parameters:
            None

        Returns:
            None
    '''

    # Define the URL and headers to scrape
    url = "https://travel.gc.ca/travelling/advisories"
    headers = ["Country", "Advisory"]

    # Scrape the webpage and parse the HTML
    table_data = get_html_table_data(url, headers)
    if table_data is None:
        return

    # Map the text advisory to an int for easier storing in database
    safety_mapping = {
        'Take normal security precautions': 1,
        'Exercise a high degree of caution': 2,
        'Avoid non-essential travel': 3,
        'Avoid all travel': 4
    }


    # Map advisory text to safety value
    table_data['safety'] = table_data['Advisory'].apply(
        lambda x: safety_mapping.get(x.split('(')[0].strip())
    )

    # Remove rows with missing safety values
    table_data = table_data.dropna(subset=['safety'])

    dbname = get_database()
    cities_collection = dbname["cities"]

    # Update city safety values in the database
    for _, row in table_data.iterrows():
        update_city_safety(cities_collection, row['Country'], row['safety'])
