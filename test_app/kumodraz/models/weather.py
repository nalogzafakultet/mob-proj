import json
from datetime import datetime
import pymongo

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

    def get_last_n_by_time(self, number):
        '''
            Retrieves last n occurences of weathers from the database
        :param number:      number of results
        :return:            weathers dict sorted by time
        '''
        try:
            sorted_weathers = self.collection.find({}, {'_id': 0}).sort('time', pymongo.DESCENDING)[:number]
            weathers = [format_object(weather) for weather in sorted_weathers]
            if sorted_weathers:
                return weathers
        except:
            print('Exception occured while getting last {} weathers.'.format(
                number
            ))
            return None

        return None

    def get_all_weathers_after(self, date, sort_order=pymongo.DESCENDING):
        try:
            weathers_after = self.collection.find({
                'time': {
                    '$gte': str(date)
                }
            }, {
                '_id': 0
            }).sort('time', sort_order)
            weathers = [format_object(weather) for weather in weathers_after]
            return weathers

        except:
            print('Error getting all weathers after {}'.format(str(date)))

        return None

    def get_n_weathers_after(self, date, number, sort_order=pymongo.DESCENDING):
        return self.get_all_weathers_after(date, sort_order)[:number]

