"""
This module provides functions for finding weather stations near a list of cities using the NOAA
API and OpenCage geocoder API.

Functions:
    read_cities(filename: str) -> List[Dict[str, str]]:
        Reads a CSV file containing city data and returns a list of dictionaries with keys
        "city", "id", and "name" corresponding to the relevant columns in the CSV file.

    calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    Calculates the distance between two locations on Earth, given their latitude and longitude
    coordinates, using the Haversine formula.

    get_bounds(city: str, country: str) -> Optional[Tuple[float, float]]:
        Given the name of a city and its country, uses the OpenCage geocoder API to retrieve the
        latitude and longitude coordinates for the city.

    get_station(params: Dict[str, Union[str, int]]) -> List[Dict[str, Union[str, int]]]:
        Given a dictionary of parameters, sends a GET request to the NOAA API and returns the
        results as a list. This function uses the retry package to handle network errors.

    get_best_station(city_name: str, stations: List[Dict[str, Union[str, int, float]]]) -> Dict[str,
    Union[str, float]]:
        Given a city name and a list of weather stations, returns the weather station that has the
        highest score, where the score is calculated based on the distance of the station from the
        city and the percentage of data coverage.

    get_country(city_name: str) -> str:
        Given a city name, retrieves the corresponding country name from a MongoDB database.

    get_stations(year: int, num_years: int, stations: List[Dict[str, Union[str, int, float]]]) ->
    List[Dict[str, Union[str, int, float]]]]:
        Given a year, a number of years, and a list of weather stations, filters the list to only
        include stations whose maxdate year is greater than or equal to the specified year and
        whose date coverage is at least num_years. The resulting list is sorted by score in
        descending order.

    main() -> None:
        Iterates through all cities from a csv file, retrieves their latitude and longitude
        coordinates, queries the NOAA API to find nearby weather stations, calculates a score for
        each station, and selects the best station for the city based on its score.

Notes:
    This module requires the following libraries to be installed: requests, csv, os, time,
    opencage.geocoder, dotenv, and retry.
    The module also requires a .env file to be present in the root directory, containing the 
    following variables: NCEI_TOKEN, OPENCAGE_API_KEY.
    The update_database script to add temperature data should be run first
"""

import requests
import os
import csv
import time
import json
from typing import Dict, List, Tuple, Optional, Union
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode
from retry import retry

import sys
sys.path.insert(0, '../..')  # Add parent directory to sys.path

from get_database import get_database
import math

# Load environment variables
load_dotenv()

# Get the API tokens and keys from environment variables
NCEI_TOKEN = os.getenv('NCEI_TOKEN')
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')

# Create a geocoder object with the OpenCage API key
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

# Get the cities collection from the database
dbname = get_database()
cities_collection = dbname["cities"]


def read_cities(filename: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file containing city data and returns a list of dictionaries with keys
    "city", "id", and "name" corresponding to the relevant columns in the CSV file.

    Parameters:
        filename (str): The path to the CSV file to be read.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary corresponds to a row
        in the CSV file and contains the "city", "id", and "name" of the city.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """

    cities = []
    with open(filename, newline="", encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            cities.append({
                "city": row[3],
                "id": row[-1],
                "name": row[2]
            })
    return cities


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the distance between two locations on Earth, given their latitude and longitude
    coordinates, using the Haversine formula.

    Parameters:
        lat1 (float): The latitude of the first location, in decimal degrees.
        lon1 (float): longitude of the first location, in decimal degrees.
        lat2 (float): The latitude of the second location, in decimal degrees.
        lon2 (float): The longitude of the second location, in decimal degrees.

    Returns:
        float: The distance between the two locations, in kilometers.

    References:
        [1] Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula
        [2] Earth radius: https://en.wikipedia.org/wiki/Earth_radius
    """

    R = 6378  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def get_bounds(city: str, country: str) -> Optional[Tuple[float, float]]:
    """
    Use the OpenCage geocoder API to get the latitude and longitude of a city and country.

    Parameters:
        city (str): The name of the city.
        country (str): The name of the country.

    Returns:
        Optional[Tuple[float, float]]: A tuple containing the latitude and longitude of the 
        specified city and country if the geocoder API returns results. If there are no results or
        an error occurs, None is returned.
    """

    # Use the OpenCage geocoder API to get the latitude and longitude of the city
    query = f"{city}, {country}"
    results = geocoder.geocode(query)
    if results:
        try:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            return (lat, lng)
        except KeyError:
            return None
    else:
        return None


@retry(tries=3, delay=5, backoff=2, jitter=(1, 3), logger=None)
def get_station(params: Dict[str, str]) -> List[Dict[str, Union[str, float]]]:
    """
    Sends a GET request to the NOAA API to retrieve a list of weather stations that match the given
    parameters. Retries the request up to 'tries' number of times if it fails.
    
    Parameters:
        params (Dict[str, str]): A dictionary of parameters to include in the API request.
            Required parameters: "limit" (the maximum number of results to return) and
            "offset" (the number of results to skip before starting to return data).
            Optional parameters: "datasetid", "startdate", "enddate", "sortfield", "sortorder",
            "stationid", "stationname", "datatypeid", "locationid".

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries, where each dictionary contains 
        information on a single weather stati

    Raises:
        ValueError: If the response status code is not 200.
    """

    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"

    # Send a GET request to the NOAA API with the given parameters and token
    response = requests.get(url, params=params, headers={
        'token': NCEI_TOKEN}, timeout=20)

    # Raise an error if the response status code is not 200
    if response.status_code != 200:
        raise ValueError("Failed to get station data.")

    # Return the results from the response as a list
    return response.json().get("results", [])


def get_best_station(city_name: str, country: str, stations: List[
    Dict[str, Union[str, float]]]) -> Optional[Dict[str, Union[str, float]]]:
    """
    Given a city name and a list of stations, return the station with the highest score and write
    its data to a CSV file.

    Parameters:
        city_name (str): The name of the city being searched.
        country (str): The name of the country being searched.
        stations (List[Dict[str, Union[str, float]]]): A list of dictionaries representing stations,
        where each dictionary contains keys 'score', 'mindate', 'maxdate', 'name', 'id', 'latitude',
        'longitude', and 'elevation'.

    Returns:
        Optional[Dict[str, Union[str, float]]]: A dictionary representing the station with the
        highest score, or None if the input list of stations is empty.
    """

    if not stations:
        return None

    # Find the station with the highest score
    best_station = max(stations, key=lambda s: s["score"])

    # Assign station data to variables
    mindate = best_station['mindate']
    maxdate = best_station['maxdate']
    name = best_station['name']
    station_id = best_station['id']
    latitude = best_station['latitude']
    longitude = best_station['longitude']
    distance = best_station['distance']
    datacoverage = best_station['datacoverage']

    # Write station data to CSV
    with open('csv/stations_improved.csv', mode='a', newline='', encoding='UTF-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([mindate, maxdate, name, city_name, country,
                        station_id, latitude, longitude, distance, datacoverage])

    return best_station


def get_country(city_name: str) -> str:
    """
    Given a city name, returns the country in which the city is located.

    Parameters:
        city_name (str): A string representing the name of the city.

    Returns:
        str: A string representing the name of the country in which the city is located.
    """
    return cities_collection.find_one({'city': city_name})['country']


def get_stations(year: str, num_years: int, data: List[Dict[str, Union[str, float]]]) -> List[
    Dict[str, Union[str, float]]]:
    """
    Filter and return a list of stations that meet certain criteria.
    The filtering is based on two conditions:
        1. The year of the "maxdate" value of each dictionary in the "data" list is greater than or 
        equal to the "year" parameter
        2. The difference between the year of the "maxdate" value and the year of the "mindate"
        value of each dictionary in the "data" list is greater than or equal to the "num_years"
        parameter.

    Note that the year is the first 4 characters of maxdate and mindate which should both exist in
    each dictionary entry of data.

    Parameters:
        year (str): The minimum year of the "maxdate" value for each station.
        num_years (int): The minimum difference between the year of the "maxdate" value and the year
            of the "mindate" value for each station.
        data (List[Dict[str, Any]]): A list of dictionaries representing station data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing station data that meet the
        criteria.
    """

    stations = [s for s in data if s["maxdate"][:4] >= year and int(
        s["maxdate"][:4]) - int(s["mindate"][:4]) >= num_years]
    return stations


def find_stations(data: List[Dict[str, Union[str, float]]]) -> List[Dict[str, Union[str, float]]]:
    """
    Find and return a list of stations that meet certain criteria.

    This function attempts to find a list of stations that have reported data in the past 20 years.
    If no stations are found with data in the past 20 years, it decreases the number of years by 5
    and tries again until it finds a list of stations or until it reaches a minimum of 5 years.

    Parameters:
        data (List[Dict[str, Union[str, float]]]): A list of dictionaries representing station data.

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries representing station data that
        meet the criteria.
    """

    # Initialize empty list of stations
    stations = []

    # Set the initial number of years to check and the year to start checking from
    num_years = 20
    year = '2020'

    # Keep decreasing the number of years to check by 5 until it reaches a minimum of 5 years
    while num_years >= 5:
        # Get the stations that have reported data in the past `num_years` years
        stations = get_stations(year, num_years, data)

        # If stations with data are found, return the list of stations
        if stations:
            return stations

        # Decrease the number of years by 5 and try again
        num_years -= 5

    # If no stations are found with data in the past 20 years, return the stations with data from
    # the year 2000. If they have not reported data since 2000 then ignore it as too outdated.
    return get_stations('2000', num_years, data)


def main() -> None:
    """
    Process a list of cities and find the best weather station for each city.

    Reads a list of cities with their respective IDs from a CSV file and retrieves
    the latitude and longitude coordinates for each city. Then, it queries the NOAA API to
    find nearby weather stations. A score is calculated for each station based on its distance from
    the city and the quality of its data. Finally, the best station for each city is selected based
    on its score.

    Parameters:
        None

    Returns:
        None
    """

    # Read all cities from CSV file
    all_cities = read_cities("csv/cities.csv")

    # Iterate through all cities and find the best weather station for each
    for city in all_cities:
        # Wait for 1 second before processing each city
        time.sleep(1)
        # Get city name, location ID, and country name
        city_name = city['city']
        locationid = city['id']
        country = get_country(city_name)

        # Print message to indicate which city is being processed
        print('Getting info for the following city:', city)

        # Get latitude and longitude for the city
        lat, lng = get_bounds(city_name, country)
        # Set parameters for the station API request
        params = {
            'datasetid': 'GHCND',
            'locationid': locationid,
            'units': 'metric',
            'limit': 1000
        }

        # Try to get station data from API, and retry once if request times out
        try:
            data = get_station(params)
        except requests.exceptions.ReadTimeout:
            print("Request timed out. Retrying after waiting for 5 seconds.")
            time.sleep(5)
            data = get_station(params)

        # Find stations to use
        stations = find_stations(data)

        # Calculate the distance to each station from the longitude and latitude values of the city
        for station in stations:
            station["distance"] = calculate_distance(
                lat, lng, station["latitude"], station["longitude"])
        
        # Assign a score to each station based on the above criteria
        for station in stations:
            station["score"] = (1 / (station["distance"])) * \
                station["datacoverage"]

        # Get the best station for the city based on score
        best_station = get_best_station(city_name, country, stations)

        # Print the best station for the city if one is found, else print a message indicating no
        # station was found
        if best_station:
            print('The best station for', city_name, 'is',
                  best_station['name'], 'with a score of', best_station['score'])
        else:
            print('No station found for', city_name)


if __name__ == '__main__':
    main()
