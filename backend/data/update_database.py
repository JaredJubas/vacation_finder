'''
A module for updating temperature and safety data in a database.

Functions:
    update_database(temperature: bool, safety: bool) -> None
        Updates the database with temperature and/or safety data if specified.

Arguments:
    temperature (bool): A boolean indicating whether to update the temperature data in the database.
    safety (bool): A boolean indicating whether to update the safety data in the database.

Example usage:
    # Call from command line to update temperature and safety data:
    # yarn update-data --temperature --safety

Notes:
    This module requires the add_temperature_data and add_safety_data modules to be imported.
    The logging level is set to INFO to write to the console.
'''

import sys
import argparse
import logging
from add_temperature_data import add_temperature_to_db
from add_safety_data import add_safety_to_db

# Set the logging level to INFO to write to console
logging.basicConfig(level=logging.INFO)

def update_database(temperature, safety):
    '''
    Updates the database with the temperature and safety data, if specified.

        Parameters:
            temperature (bool): A boolean indicating whether to update the temperature data in the 
            database.
            safety (bool): A boolean indicating whether to update the safety data in the database.

        Returns:
            None
    '''
    if temperature:
        logging.info('Updating temperature data')
        add_temperature_to_db()

    if safety:
        logging.info('Updating safety data')
        add_safety_to_db()


if __name__ == "__main__":
    # Default value for boolean argument is False
    # Command line call example: yarn update-data --temperature --safety
    parser = argparse.ArgumentParser(description='Update data')
    parser.add_argument('--temperature', action='store_true',
                        help='If temperature data should be updated')
    parser.add_argument('--safety', action='store_true',
                        help='If safety data should be updated')
    args = parser.parse_args(sys.argv[1:])

    update_database(args.temperature, args.safety)
