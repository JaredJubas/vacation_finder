from flask import Flask, request
from get_cities import get_cities
from get_database import get_database

api = Flask(__name__)


@api.route('/cities')
def my_profile():
    minTemp = request.args.get('minTemp')
    maxTemp = request.args.get('maxTemp')
    month = request.args.get('month')

    dbname = get_database()

    response = get_cities(minTemp, maxTemp, month, dbname)

    return response
