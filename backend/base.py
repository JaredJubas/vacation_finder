from flask import Flask, request
from get_cities import get_cities

api = Flask(__name__)


@api.route('/cities')
def my_profile():
    minTemp = request.args.get('minTemp')
    maxTemp = request.args.get('maxTemp')
    month = request.args.get('month')

    response = get_cities(minTemp, maxTemp, month)

    return response
