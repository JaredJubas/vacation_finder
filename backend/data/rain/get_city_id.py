"""
This module provides a function to retrieve city data from a MongoDB database and the NOAA API, and
write the data to a CSV file.

Functions:
    get_cities_data() -> None
        Retrieves data on cities from the NOAA API and writes it to a CSV file. Filters the API
        results to only include cities already present in the database.
        API documentation: https://www.ncdc.noaa.gov/cdo-web/webservices/v2#locations

Example usage:
    # Call from command line:
    # python get_city_id.py

Notes:
    This module requires the following libraries to be installed: 
    requests, csv, os, dotenv, pymongo.
    The module also requires a .env file to be present in the root directory, containing the
    following variable: NCEI_TOKEN.
    The get_database function is imported from a separate module, which should contain the necessary
    code to establish a connection to the MongoDB database.
"""

import requests
import os
import csv
from dotenv import load_dotenv

import sys
sys.path.insert(0, '../..')  # Add parent directory to sys.path

from get_database import get_database

# Load environment variables
load_dotenv()

# Get NCEI API token from environment variables
NCEI_TOKEN = os.getenv('NCEI_TOKEN')

# Get database and cities collection
dbname = get_database()
cities_collection = dbname["cities"]


def get_cities_data() -> None:
    """
    Retrieves data for all cities available from the NOAA API and saves it to a CSV file.
    Continuously updates the API's offset parameter until all available data has been retrieved.

    Parameters:
        None

    Returns:
        None

    Raises:
        HTTPError: If the initial API call fails, or if subsequent calls return an HTTP error.
    """

    # Get a list of all cities in the database
    cities = cities_collection.distinct('city')

    # Set up the initial API parameters for the first request
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/locations"
    params = {
        'datasetid': 'GHCND',  # Only get data from this dataset
        'locationcategoryid': 'CITY',  # Only get data for cities
        'limit': 1000,  # Get up to 1000 results per request
        'offset': 0  # Start with the first result
    }

    while True:
        # Make the API request
        response = requests.get(url, params=params, headers={
            'token': NCEI_TOKEN}, timeout=20)

        # Get the data from the response
        data = response.json().get("results", [])

        # If no data is returned, we've got all the data and can break out of the loop
        if not data:
            break

        # Write the data to the CSV file
        with open('csv/cities.csv', mode='a', newline='', encoding='UTF-8') as csv_file:
            writer = csv.writer(csv_file)

            for result in data:
                name = result['name']
                split_name = name.split(',')
                city = split_name[0]

                # Only write the city if it exists in the DB
                if city in cities:
                    mindate = result['mindate']
                    maxdate = result['maxdate']
                    city_id = result['id']
                    writer.writerow([mindate, maxdate, name, city, city_id])

        # Update the offset for the next request
        params['offset'] += len(data)


if __name__ == "__main__":
    get_cities_data()
