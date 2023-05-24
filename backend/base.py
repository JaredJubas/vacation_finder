from flask import Flask, request
from flask_cors import CORS
from get_cities import get_cities
from get_database import get_database

api = Flask(__name__)
CORS(api)


@api.route('/cities')
def my_profile():
    min_temp = request.args.get('minTemp')
    max_temp = request.args.get('maxTemp')
    month = request.args.get('month')
    rainy_days = request.args.get('rainyDays')

    dbname = get_database()

    response = get_cities(min_temp, max_temp, month, rainy_days, dbname)

    return response
