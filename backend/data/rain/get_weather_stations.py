"""
This module provides functions to retrieve weather station data from the NOAA API, geocode city
names to get bounding coordinates, and write station data to a CSV file.

Functions:
    get_bounds(city: str, country: str) -> tuple
        Geocodes a city name and country to retrieve bounding coordinates using the OpenCage API.
        API documentation: https://opencagedata.com/api

    write_to_csv(station_data: dict, city: str, country: str) -> None
        Appends station data to a CSV file.

    get_station_data(params: dict) -> dict
        Retrieves station data from the NOAA API given a set of parameters.
        API documentation: https://www.ncdc.noaa.gov/cdo-web/webservices/v2#stations

    get_station(city: str, country: str, radius: float = 0.5) -> None
        Retrieves station data for a given city and writes it to a CSV file.

    get_stations_for_cities_in_database() -> None
        Retrieves station data for all cities in a MongoDB database and writes it to a CSV file.

Example usage:
    # Call from command line:
    # python get_weather_stations.py

Notes:
    This module requires the following libraries to be installed: requests, csv, os, logging, time,
    opencage.geocoder, dotenv, and retry.
    The module also requires a .env file to be present in the root directory, containing the 
    following variables: NCEI_TOKEN, OPENCAGE_API_KEY.
    The update_database script to add temperature data should be run first
"""

from typing import Optional, Tuple
import csv
import os
import logging
import time
import sys
import requests
from opencage.geocoder import OpenCageGeocode
from dotenv import load_dotenv
from retry import retry

sys.path.insert(0, '../..')  # Add parent directory to sys.path

from get_database import get_database


# Load environment variables
load_dotenv()

# Get NCEI API token and OpenCage API key from environment variables
NCEI_TOKEN = os.getenv('NCEI_TOKEN')
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')

# Get database and cities collection
dbname = get_database()
cities_collection = dbname["cities"]

# Set up OpenCage Geocoding API
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)


def get_bounds(city: str, country: str) -> Optional[Tuple[float, float, float, float]]:
    """
    Get the latitude and longitude bounds (northeast and southwest) for a given city and country.

    Parameters:
        city (str): The name of the city to look up.
        country (str): The name of the country to look up.

    Returns:
        Optional[Tuple[float, float, float, float]]: A tuple of four floats representing the
        latitude and longitude bounds of the city, in the order northeast latitude, northeast
        longitude, southwest latitude, southwest longitude. If the city and country cannot be
        geocoded or the bounds cannot be found, returns None.
    """

    # Build geocoding query string
    query = f"{city}, {country}"

    # Geocode the query and get results
    results = geocoder.geocode(query)

    # If results are found, get the bounds and return as a tuple of floats
    if results:
        try:
            northeast = results[0]['bounds']['northeast']
            southwest = results[0]['bounds']['southwest']
            return (northeast['lat'], northeast['lng'], southwest['lat'], southwest['lng'])
        # If the bounds cannot be found in the results, return None
        except KeyError:
            return None
    # If no results are found, return None
    else:
        return None


def write_to_csv(station_data: dict, city: str, country: str) -> None:
    """
    Writes station data to a CSV file. The information written should be mindate, maxdate, name, 
    city, country, id, latitude, and longitude.

    Parameters:
        station_data (dict): A dictionary containing information about a weather station.
        city (str): The name of the city where the weather station is located.
        country (str): The name of the country where the weather station is located.

    Returns:
        None
    """

    # Extract relevant data from station_data dictionary
    mindate = station_data['mindate']
    maxdate = station_data['maxdate']
    name = station_data['name']
    station_id = station_data['id']
    latitude = station_data['latitude']
    longitude = station_data['longitude']

    # Write data to CSV file
    with open('csv/stations.csv', mode='a', newline='', encoding='UTF-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([mindate, maxdate, name, city, country,
                        station_id, latitude, longitude])


@retry(tries=3, delay=5, backoff=2, jitter=(1, 3), logger=None)
def get_station_data(params: dict) -> dict:
    """
    Retrieves data from the NOAA API for stations and returns a JSON object of the response.

    Parameters:
        params (dict): A dictionary of parameters to pass to the API endpoint.

    Returns:
        dict: A JSON object of the API response.

    Raises:
        ValueError: If the response status code is not 200 (i.e. the request failed).
    """

    # define the API endpoint URL
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"

    # make a GET request to the API with the specified parameters and token header
    response = requests.get(url, params=params, headers={
        'token': NCEI_TOKEN}, timeout=10)

    # raise a ValueError if the response status code is not 200
    if response.status_code != 200:
        raise ValueError("Failed to get rainfall data.")

    # return the JSON response from the API
    return response.json()


def get_station(city: str, country: str, radius: float = 0.5) -> None:
    """
    Gets a weather station within a specified radius of a given city and write it to a csv file. The 
    weather station used should be the one with the latest maxdate. 

    Parameters:
        city (str): The name of the city.
        country (str): The name of the country.
        radius (float, optional): The radius around the city in degrees. Defaults to 0.5.

    Returns:
        None: The function does not return anything but writes the data to a CSV file.
    """

    # get the geographic bounds of the city
    bounds = get_bounds(city, country)

    # set the parameters for the API request
    params = {
        'datasetid': 'GHCND'
    }

    # if bounds were successfully retrieved, add the extent parameter to the API request
    if bounds:
        # the extent parameter is a bounding box defined by four coordinates: xmin, ymin, xmax, ymax
        params['extent'] = {bounds[2] - radius}, {bounds[3] - radius}, {bounds[0] + radius}, {
            bounds[1] + radius}

        try:
            # make a request to the API to get the station data
            data = get_station_data(params)
        except requests.exceptions.ReadTimeout:
            # if the request times out, wait for 5 seconds and try again
            print("Request timed out. Retrying after waiting for 5 seconds.")
            time.sleep(5)
            data = get_station_data(params)

        try:
            # get the station with the latest maxdate
            station = max(data["results"], key=lambda x: x["maxdate"])
            # write the station data to a CSV file
            write_to_csv(station, city, country)
        except KeyError:
            # if no stations were found for the city and country, log an error message
            logging.error(
                "No stations found for city %s in country %s", city, country)
    else:
        # if bounds could not be retrieved for the city and country, print an error message
        print(f"Could not get bounds for {city}, {country}.")


def get_stations_for_cities_in_database() -> None:
    """
    This function retrieves the cities from the MongoDB database and gets the weather stations for
    each city by calling the 'get_station()' function.

    Parameters:
        None

    Returns:
        None
    """

    # Loop through all documents in the 'cities_collection' collection
    for document in cities_collection.find():
        # Get the name of the city and country from the current document
        city = document['city']
        country = document['country']

        # Add a wait statement to avoid hitting the API rate limit
        time.sleep(1)

        # Call the get_station() function to retrieve weather station data for the city and country
        get_station(city, country)


if __name__ == "__main__":
    # Call the 'get_stations_for_cities_in_database()' function when the script is run
    get_stations_for_cities_in_database()
