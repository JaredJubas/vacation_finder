"""
This module provides functions to retrieve rainfall data for weather stations using the NOAA API,
and save the data to a database and CSV file.

Functions:
    read_stations(filename: str) -> list
        Reads a CSV file containing weather station information, and returns a list of dictionaries
        where each dictionary represents a weather station.

    get_rain_data(params: dict) -> list
        Retrieves rainfall data from the NOAA API, given a dictionary of parameters. If the request
        fails, it will retry up to 3 times before raising an error.
        API documentation: https://www.ncdc.noaa.gov/cdo-web/webservices/v2

    count_rainy_days(max_date: datetime, min_date: datetime, station_id: str) -> tuple
        Counts the number of rainy days and total precipitation for each month, given a weather
        station's maximum and minimum dates of observation, and the station ID. Returns a tuple
        containing two dictionaries: one containing the average number of rainy days per month over
        the past 20 years, and the other containing the average total precipitation per month over
        the past 20 years.

    update_db_with_rain(city: str, country: str, rainy_days: dict, total_precipitation: dict, 
                        name: str, id: str) -> None
        Saves rainfall data for a weather station to a MongoDB database and a CSV file, given the
        city name, country, dictionaries of average rainy days and total precipitation per month,
        the station name, and the station ID.
    
    add_rain_to_db() -> None
        Main function that updates the average monthly rainfall values in the database.
"""


import requests
import os
import csv
import time
from dotenv import load_dotenv
from datetime import datetime
from retry import retry

import sys
sys.path.insert(0, '..')  # Add parent directory to sys.path

from get_database import get_database

load_dotenv()

NCEI_TOKEN = os.getenv('NCEI_TOKEN')

MONTH_NAMES = ["jan", "feb", "mar", "apr", "may",
               "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

def read_stations(filename: str)-> list:
    """
    Read a CSV file containing weather station information and return a list of dictionaries
    representing each station.

    Parameters:
        filename (str): The path to the CSV file to read.

    Returns:
        list: A list of dictionaries representing each station in the CSV file. Each dictionary has
        the following keys:
            mindate: The earliest date for which the station has data.
            maxdate: The latest date for which the station has data.
            name: The name of the station.
            city: The city in which the station is located.
            country: The country in which the station is located.
            id: The unique identifier for the station.
    """

    stations = []
    with open(filename, newline="", encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header row
        for row in reader:
            stations.append({
                "mindate": datetime.strptime(row[0], "%Y-%m-%d"),
                "maxdate": datetime.strptime(row[1], "%Y-%m-%d"),
                "name": row[2],
                "city": row[3],
                "country": row[4],
                "id": row[5],
            })
    return stations


@retry(tries=3, delay=5, backoff=2, jitter=(1, 3), logger=None)
def get_rain_data(params: dict) -> list:
    """
    Retrieves data from the NOAA API for percipitation and returns a list of the results.

    Parameters:
        params (dict): A dictionary of parameters to pass to the API endpoint.

    Returns:
        list: A list of dictionaries representing percipitation data from the API.
        Each dictionary in the list represents a single observation and has the following keys:
            date: A datetime object representing the date of the observation.
            value: A float representing the amount of percipitation in millimeters.
    
    Raises:
        ValueError: If the response status code is not 200 (i.e. the request failed).
    """

    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"

    response = requests.get(url, params=params, headers={
        'token': NCEI_TOKEN}, timeout=20)

    if response.status_code != 200:
        raise ValueError("Failed to get rainfall data.")

    return response.json().get("results", [])


def count_rainy_days(max_date: datetime, min_date: datetime, station_id: str) -> tuple:
    """
    Calculates the average number of rainy days and total precipitation per month for a given
    weather station ID, averaged over 20 years. If there is not 20 years of data then use as many
    that is available. Assume no rain on any day that has no data.

    Parameters:
        max_date (datetime): the latest date to include in the calculations
        min_date (datetime): the earliest date to include in the calculations
        station_id (str): the weather station ID to retrieve data from

    Returns:
        tuple: A tuple of two dictionaries, containing the average number of rainy days and total
        precipitation per month, respectively. The keys of both dictionaries are the abbreviated
        month names (e.g. "jan", "feb", etc.).
    """

    rainy_days_per_month = {month: 0 for month in MONTH_NAMES}
    total_precipitation_per_month = {month: 0 for month in MONTH_NAMES}

    for year_offset in range(1, 21):
        year = max_date.year - year_offset
        year_start = datetime(year, 1, 1)
        year_end = datetime(year, 12, 31)

        # min_date is the earliest date that data could be available
        # To ensure a full year of data, add 1 to the min_date
        if min_date.year + 1 > year:
            break

        params = {
            "stationid": station_id,
            "datasetid": "GHCND",
            "startdate": year_start.date().isoformat(),
            "enddate": year_end.date().isoformat(),
            "datatypeid": "PRCP",
            "limit": 1000,
            "units": "metric",
            "includemetadata": False,
        }

        time.sleep(0.2)

        try:
            data = get_rain_data(params)
        except requests.exceptions.ReadTimeout:
            print("Request timed out. Retrying after waiting for 5 seconds.")
            time.sleep(5)
            data = get_rain_data(params)

        for observation in data:
            # Note: if no data is available for a certain day then assume 0
            date = datetime.strptime(observation["date"], "%Y-%m-%dT%H:%M:%S")
            month_name = date.strftime("%b").lower()
            precipitation = observation["value"]
            if precipitation is not None and float(precipitation) >= 1.0:
                rainy_days_per_month[month_name] += 1
            if precipitation is not None:
                total_precipitation_per_month[month_name] += float(
                    precipitation)

    for month in MONTH_NAMES:
        rainy_days_per_month[month] /= min(20, max_date.year - min_date.year - 1)
        rainy_days_per_month[month] = round(rainy_days_per_month[month], 2)

        total_precipitation_per_month[month] /= min(
            20, max_date.year - min_date.year - 1)
        total_precipitation_per_month[month] = round(total_precipitation_per_month[month], 2)

    return rainy_days_per_month, total_precipitation_per_month


def update_db_with_rain(station_data: dict, days_rainy: dict, total_rain: dict) -> None:
    """
    Adds rainfall data for a given weather station to the database and a CSV file.

    Parameters:
        station_data (dict): A dictionary representing the weather station, which must contain keys
            'city', 'country', 'name', and 'id' with string values.
        days_rainy (dict): A dictionary with keys representing the abbreviated month names (e.g.,
            'jan') and values representing the average number of rainy days for each month over a
            span of up to 20 years.
        total_rain (dict): A dictionary with keys representing the abbreviated month names
            (e.g., 'jan') and values representing the average total precipitation in millimeters for
            each month over a span of up to 20 years.

    Returns:
        None
    """

    city = station_data['city']
    country = station_data['country']
    name = station_data['name']
    station_id = station_data['id']

    dbname = get_database()
    cities_collection = dbname["cities"]

    for month in days_rainy:
        cities_collection.update_one(
            {'city': city, 'country': country},
            {'$set': {f"months.{month}.rain": days_rainy[month]}}
        )

    # Currently only average number of rainy days is written to the database, but store average 
    # total rainfall per month in a csv file just in case it is needed later, that way we won't have 
    # to make all the API calls again
    with open('rain.csv', mode='a', newline='', encoding='UTF-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([city, country, name, station_id,
                        days_rainy, total_rain])


def add_rain_to_db() -> None:
    """
    Main function that updates the average number of rainy days in the database.

        Parameters:
            None

        Returns:
            None
    """

    all_stations = read_stations("stations.csv")
    for station in all_stations:
        print('Getting info for the following station:', station)
        rainy_days, total_precipitation = count_rainy_days(station["maxdate"], station["mindate"],
                                                           station["id"])
        update_db_with_rain(station, rainy_days, total_precipitation)
