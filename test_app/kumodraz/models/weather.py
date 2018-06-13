import json
from datetime import datetime
import pymongo
from bson import ObjectId
from dateutil.relativedelta import relativedelta

from kumodraz.utils.config import DB_COLLECTION_NAME, DATE_FORMAT, DAY_FORMAT

def format_object(weather):
    for key in weather:
        if key == 'vreme':
            weather[key] = datetime.strptime(weather[key], DATE_FORMAT)
    return weather

def format_fo_api(weather):
    for key in weather:
        if key == 'vreme':
            weather[key] = int(unix_time_millis(datetime.strptime(weather[key], DATE_FORMAT)))
    return weather

def weathers_stats(weathers):

    if len(weathers) == 0:
        return {}

    ret = {
        'min_temperatura': -500.0,
        'max_temperatura': 500.0,
        'min_osvetljenje': -500.0,
        'max_osvetljenje': 500.0,
        'min_pritisak': -500.0,
        'max_pritisak': 500.0,
        'min_vlaznost': -500.0,
        'max_vlaznost': 500.0,
    }

    for weather in weathers:
        if weather['pritisak'] > ret['max_pritisak']:
            ret['max_pritisak'] = weather['pritisak']
        if weather['pritisak'] < ret['min_pritisak']:
            ret['min_pritisak'] = weather['pritisak']
        if weather['osvetljenje'] > ret['max_osvetljenje']:
            ret['max_osvetljenje'] = weather['osvetljenje']
        if weather['osvetljenje'] < ret['min_osvetljenje']:
            ret['min_osvetljenje'] = weather['osvetljenje']
        if weather['temperatura'] > ret['max_temperatura']:
            ret['max_temperatura'] = weather['temperatura']
        if weather['temperatura'] < ret['min_temperatura']:
            ret['min_temperatura'] = weather['temperatura']
        if weather['vlaznost'] > ret['max_vlaznost']:
            ret['max_vlaznost'] = weather['vlaznost']
        if weather['vlaznost'] < ret['min_vlaznost']:
            ret['min_vlaznost'] = weather['vlaznost']

    return ret


def aggregate_stats(stats):
    if len(stats) == 0:
        return {}

    sum_min_tmp = 0.0
    sum_max_tmp = 0.0
    sum_min_vlaz = 0.0
    sum_max_vlaz = 0.0
    sum_min_pritisak = 0.0
    sum_max_pritisak = 0.0
    sum_min_osvetljenje = 0.0
    sum_max_osvetljenje = 0.0

    for stat in stats:
        sum_min_tmp += stat['min_temperatura']
        sum_max_tmp += stat['max_temperatura']
        sum_min_vlaz += stat['min_vlaznost']
        sum_max_vlaz += stat['max_vlaznost']
        sum_min_pritisak += stat['min_pritisak']
        sum_max_pritisak += stat['max_pritisak']
        sum_min_osvetljenje += stat['min_osvetljenje']
        sum_max_osvetljenje += stat['max_osvetljenje']

    ret = {
        "avg_min_temp": sum_min_tmp / len(stats),
        "avg_max_temp": sum_max_tmp / len(stats),
        "avg_min_vlaz": sum_min_vlaz / len(stats),
        "avg_max_vlaz": sum_max_vlaz / len(stats),
        "avg_min_osvetljenje": sum_min_osvetljenje / len(stats),
        "avg_max_osvetljenje": sum_max_osvetljenje / len(stats),
        "avg_min_pritisak": sum_min_pritisak / len(stats),
        "avg_max_pritisak": sum_max_pritisak / len(stats)
    }


def statistics(weathers):
    if len(weathers) == 0:
        return {}

    ret = {
        'min_temperatura': 500.0,
        'max_temperatura': -500.0,
        'min_osvetljenje': 500,
        'max_osvetljenje': -500,
        'min_brzina': 500.0,
        'max_brzina': -500.0,
        'min_vlaznost': 500.0,
        'max_vlaznost': -500.0
    }

    sum_vlaz = 0
    sum_t = 0
    sum_brz = 0
    sum_osv = 0
    for weather in weathers:
        if weather['brzina_vetra'] > ret['max_brzina']:
            ret['max_brzina'] = weather['brzina_vetra']
        if weather['brzina_vetra'] < ret['min_brzina']:
            ret['min_brzina'] = weather['brzina_vetra']
        if weather['osvetljenje'] > ret['max_osvetljenje']:
            ret['max_osvetljenje'] = weather['osvetljenje']
        if weather['osvetljenje'] < ret['min_osvetljenje']:
            ret['min_osvetljenje'] = weather['osvetljenje']
        if weather['temperatura'] > ret['max_temperatura']:
            ret['max_temperatura'] = weather['temperatura']
        if weather['temperatura'] < ret['min_temperatura']:
            ret['min_temperatura'] = weather['temperatura']
        if weather['vlaznost'] > ret['max_vlaznost']:
            ret['max_vlaznost'] = weather['vlaznost']
        if weather['vlaznost'] < ret['min_vlaznost']:
            ret['min_vlaznost'] = weather['vlaznost']

        sum_vlaz += weather['vlaznost']
        sum_t += weather['temperatura']
        sum_brz += weather['brzina_vetra']
        sum_osv += weather['osvetljenje']

    ret['avg_vlaznost'] = sum_vlaz / len(weathers)
    ret['avg_temperatura'] = sum_t / len(weathers)
    ret['avg_osvetljenje'] = sum_osv / len(weathers)
    ret['avg_brzina'] = sum_brz / len(weathers)

    return ret

epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

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
            all_weathers = [format_object(weather) for weather in self.collection.find()]
            return all_weathers
        except:
            print('Error getting all weathers')

        return None
    
    def get_weather_for_date(self, start_date, end_date):
        
        try:
            # start_date = datetime.strptime(date, DAY_FORMAT)
            # end_date = start_date + timedelta(days=1)

            # print('Start: {}'.format(str(start_date)))
            # print('End: {}'.format(str(end_date)))

            all_weathers = [format_fo_api(weather) for weather in self.collection.find({
                    'vreme': {
                        '$gte': str(start_date),
                        '$lt': str(end_date)
                    }
            }, {'_id': 0}).sort('vreme', pymongo.DESCENDING)]

            ret = {"data": all_weathers}
            return ret

        except:
            print('Error getting day weathers')

        return {}

    def get_stats_for_date(self, start_date, end_date):
        
        try:

            all_weathers = [format_fo_api(weather) for weather in self.collection.find({
                    'vreme': {
                        '$gte': str(start_date),
                        '$lt': str(end_date)
                    }
            }, {'_id': 0})]

            return statistics(all_weathers)

        except Exception as e:
            print('Error getting day weathers')
            print('Exception:', str(e))

        return {}

    def stats_per_month(self, month, year):

        current_date = datetime(year, month, 1)
        end_date = current_date + relativedelta(months=1)

        stats = []

        while current_date < end_date:
            stats.append(self.get_stats_for_date(current_date, current_date + relativedelta(days=1)))
            current_date += relativedelta(days=1)

        ret = {"data": stats}
        print('ret:', ret)
        return ret

    def get_last_n_by_time(self, number):
        '''
            Retrieves last n occurences of weathers from the database
        :param number:      number of results
        :return:            weathers dict sorted by time
        '''
        try:
            sorted_weathers = self.collection.find().sort('vreme', pymongo.DESCENDING)[:number]
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
                'vreme': {
                    '$gte': str(date)
                }
            }).sort('vreme', sort_order)
            weathers = [format_object(weather) for weather in weathers_after]
            return None

        except:
            print('Error getting all weathers after {}'.format(str(date)))

        return None

    def get_n_weathers_after(self, date, number, sort_order=pymongo.DESCENDING):
        return self.get_all_weathers_after(date, sort_order)[:number]


    def get_weather_by_id(self, id):
        return self.collection.find_one({
            '_id': ObjectId(id)
        }, {'_id': 0})
