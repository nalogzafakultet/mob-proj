import json
from datetime import datetime

from kumodraz.utils.config import DB_COLLECTION_NAME, DATE_FORMAT

def format_object(weather):
    for key in weather:
        if key == 'time':
            weather[key] = datetime.strptime(weather[key], DATE_FORMAT)
    return weather

class Weather:

    def __init__(self, db):
        self.db = db
        self.collection = db[DB_COLLECTION_NAME]

    def get_all(self):
        """

        :rtype: list
        """
        try:
            # Finds all weathers in database, excludes ids from the query
            all_weathers = [format_object(weather) for weather in self.collection.find({}, {'_id': 0})]
            return all_weathers
        except:
            print('Error getting all weathers')

        return None

    def get_last_10(self):
        try:
            last_ten = self.collection.find().sort({"date": -1}).limit(10)

            if last_ten:
                return last_ten
        except:
            print('Exception occured while getting last 10 weathers.')
            return None

        return None

    def get_x(self):
        return 5
