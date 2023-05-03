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
        API documentation: https://www.ncdc.noaa.gov/cdo-web/webservices/v2

    get_station(city: str, country: str, radius: float = 0.5) -> None
        Retrieves station data for a given city and writes it to a CSV file.

    get_stations_for_cities_in_database() -> None
        Retrieves station data for all cities in a MongoDB database and writes it to a CSV file.

    Example usage:
        # Call from command line:
        # python get_weather_stations.py

Notes:
    This module requires the following libraries to be installed: requests, csv, os, logging, time,
    opencage.geocoder, country_converter, dotenv, and retry.
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
from country_converter import CountryConverter
from dotenv import load_dotenv
from retry import retry

sys.path.insert(0, '..')  # Add parent directory to sys.path

from get_database import get_database


load_dotenv()

NCEI_TOKEN = os.getenv('NCEI_TOKEN')

OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')

dbname = get_database()
cities_collection = dbname["cities"]

# Set up OpenCage Geocoding API
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
converter = CountryConverter()


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

    query = f"{city}, {country}"
    results = geocoder.geocode(query)
    if results:
        try:
            northeast = results[0]['bounds']['northeast']
            southwest = results[0]['bounds']['southwest']
            return (northeast['lat'], northeast['lng'], southwest['lat'], southwest['lng'])
        except KeyError:
            return None
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

    mindate = station_data['mindate']
    maxdate = station_data['maxdate']
    name = station_data['name']
    station_id = station_data['id']
    latitude = station_data['latitude']
    longitude = station_data['longitude']
    with open('stations.csv', mode='a', newline='', encoding='UTF-8') as csv_file:
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

    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"

    response = requests.get(url, params=params, headers={
        'token': NCEI_TOKEN}, timeout=10)

    if response.status_code != 200:
        raise ValueError("Failed to get rainfall data.")

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

    bounds = get_bounds(city, country)
    params = {
        'datasetid': 'GHCND'
    }

    if bounds:
        params['extent'] = {bounds[2] - radius}, {bounds[3] - radius}, {bounds[0] + radius}, {
            bounds[1] + radius}
        try:
            data = get_station_data(params)
        except requests.exceptions.ReadTimeout:
            print("Request timed out. Retrying after waiting for 5 seconds.")
            time.sleep(5)
            data = get_station_data(params)

        try:
            # Get the station with the latest maxdate. Assumption is that this one will have most
            # up to date data
            station = max(data["results"], key=lambda x: x["maxdate"])
            write_to_csv(station, city, country)
        except KeyError:
            logging.error(
                "No stations found for city %s in country %s", city, country)
    else:
        print(f"Could not get bounds for {city}, {country}.")


def get_stations_for_cities_in_database() -> None:
    '''
    This function retrieves the cities from the MongoDB database and gets the weather stations for
    each city by calling the 'get_station()' function.

    Parameters:
        None

    Returns:
        None
    '''

    for document in cities_collection.find():
        city = document['city']
        country = document['country']

        # Add a wait statement to avoid hitting the API rate limit
        time.sleep(1)
        get_station(city, country)


if __name__ == "__main__":
    get_stations_for_cities_in_database()
