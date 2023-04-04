from pymongo import MongoClient
import os
from dotenv import load_dotenv


def get_database():
    load_dotenv()

    MONGODB_URI = os.getenv('MONGODB_URI')
    MONGODB_DB = os.getenv('MONGODB_DB')

    if not MONGODB_URI:
        raise Exception('Please define MONGODB_URI in .env')

    if not MONGODB_DB:
        raise Exception('Please define MONGODB_DB in .env')

    # Provide the mongodb atlas url to connect python to mongodb using pymongo

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(MONGODB_URI)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[MONGODB_DB]


if __name__ == "__main__":

    # Get the database
    dbname = get_database()
