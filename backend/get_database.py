'''
Gets the database where data for this project is being stored.

Functions:
    get_database() -> Database
'''

import os
from pymongo import MongoClient
from dotenv import load_dotenv


def get_database():
    '''
    Returns a database that is being used for this project.

        Returns:
            dbname (Database): A MongoDB database for this project
    '''

    load_dotenv()

    MONGODB_URI = os.getenv('MONGODB_URI')
    MONGODB_DB = os.getenv('MONGODB_DB')

    if not MONGODB_URI:
        raise NameError('Please define MONGODB_URI in .env')

    if not MONGODB_DB:
        raise NameError('Please define MONGODB_DB in .env')

    client = MongoClient(MONGODB_URI)

    dbname = client[MONGODB_DB]

    return dbname
