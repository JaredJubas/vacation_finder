from get_database import get_database


def get_cities(min_temp, max_temp, month):
    dbname = get_database()
    cities_collection = dbname["cities"]

    cities = list(cities_collection.find({
        "months.{}.temperature".format(month): {
          "$lte": float(max_temp), 
          "$gte": float(min_temp)
          }
    }, {
        '_id': 0,
        'city': 1,
        'country': 1,
        "months.{}.temperature".format(month): 1
    }))

    return cities


if __name__ == '__main__':
    print(get_cities(1, 2, 'jan'))
