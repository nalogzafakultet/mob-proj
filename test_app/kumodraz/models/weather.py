import json
from datetime import datetime
import pymongo
from bson import ObjectId
from dateutil.relativedelta import relativedelta

from kumodraz.utils.config import DB_COLLECTION_NAME, DATE_FORMAT, DAY_FORMAT, DB_COLLECTION_STATS_DAY, DB_COLLECTION_STATS_MONTH, DB_COLLECTION_STATS_YEAR

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


epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

class Weather:

    def __init__(self, db):
        self.db = db
        self.collection = db[DB_COLLECTION_NAME]
        self.collection_stats_day = db[DB_COLLECTION_STATS_DAY]
        self.collection_stats_month = db[DB_COLLECTION_STATS_MONTH]
        self.collection_stats_year = db[DB_COLLECTION_STATS_YEAR]

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

    def get_last(self):

        try:
            weather = self.collection.find({}, {'_id': 0}).sort('vreme', pymongo.DESCENDING)[0]
            return weather

        except:
            return None


    def get_stats_for_day(self, start_date, end_date):
        
        try:

            print('Start Date: {}'.format(start_date))
            print('End Date: {}'.format(end_date))

            stats = self.collection_stats_day.find({
                    'date': {
                        '$gte': str(start_date),
                        '$lt': str(end_date)
                    }
            }, {'_id': 0})[0]

            if stats is None:
                return {}
            else:
                return stats

        except Exception as e:
            print('Error getting day weathers')
            print('Exception:', str(e))

            return {}


    def get_stats_for_month(self, start_date, end_date):

        try:

            print('Start Date: {}'.format(start_date))
            print('End Date: {}'.format(end_date))

            stats = self.collection_stats_month.find({
                'date': {
                    '$gte': str(start_date),
                    '$lt': str(end_date)
                }
            }, {'_id': 0})[0]


            if stats is None:
                return {}
            else:
                return stats

        except Exception as e:
            print('Error getting day weathers')
            print('Exception:', str(e))

        return {}

    def get_new_stats_for_month(self, start_date, end_date):

        try:
            res = []
            curr_start = start_date
            curr_end = start_date + relativedelta(days=1)

            while curr_start < end_date:
                ret = self.get_stats_for_day(curr_start, curr_end)
                res.append(ret)
                curr_start = curr_end
                curr_end = curr_end + relativedelta(days=1)

            return res


        except Exception as e:
            print('Error getting day weathers')
            print('Exception:', str(e))

        return {}

    def get_recent_weather(self, hours=1):
        last_weather = self.collection.find({}, {'_id': 0}).sort('vreme', pymongo.DESCENDING)[0]
        end_time = datetime.strptime(last_weather['vreme'], DATE_FORMAT)
        start_time = end_time - relativedelta(hours=hours)

        try:
            all_weathers = [format_fo_api(weather) for weather in self.collection.find({
                'vreme': {
                    '$gte': str(start_time),
                    '$lt': str(end_time)
                }
            }, {'_id': 0}).sort('vreme', pymongo.DESCENDING)]

            if all_weathers is not None and len(all_weathers) > 0:
                return all_weathers

            return {}

        except:
            print('Error getting all weathers after {}'.format(str(start_date)))

        return {}


    def new_stats_for_year(self, year):
        y = int(year)
        curr_start_date = datetime(y, 1, 1)
        curr_end_date = curr_start_date + relativedelta(months=1)
        end_date = datetime(y+1, 1, 1)

        res = []
        try:
            while curr_start_date < end_date:
                stats = self.collection_stats_month.find({
                'date': {
                    '$gte': str(curr_start_date),
                    '$lt': str(curr_end_date)
                }
            }, {'_id': 0})
                agg_stats = [s for s in stats]
                if len(agg_stats) > 0:
                    res.append(agg_stats[0])
                else:
                    res.append({})
                curr_start_date = curr_end_date
                curr_end_date = curr_end_date + relativedelta(months=1)

            return res
        except Exception as e:
            print('EXCEPTION NEW STATS %s' % str(e))
            return []

    def new_stats_for_month(self, year, month):
        y = int(year)
        m = int(month)
        curr_start_date = datetime(y, m, 1)
        curr_end_date = curr_start_date + relativedelta(days=1)
        end_date = datetime(y, m+1, 1)

        res = []
        try:
            while curr_start_date < end_date:
                stats = self.collection_stats_day.find({
                'date': {
                    '$gte': str(curr_start_date),
                    '$lt': str(curr_end_date)
                }
            }, {'_id': 0})
                agg_stats = [s for s in stats]
                if len(agg_stats) > 0:
                    res.append(agg_stats[0])
                else:
                    res.append({})
                curr_start_date = curr_end_date
                curr_end_date = curr_end_date + relativedelta(days=1)

            return res
        except Exception as e:
            print('EXCEPTION NEW STATS %s' % str(e))
            return []

    def get_stats_for_year(self, start_date, end_date):

        try:

            print('Start Date: {}'.format(start_date))
            print('End Date: {}'.format(end_date))

            stats = self.collection_stats_year.find({
                'date': {
                    '$gte': str(start_date),
                    '$lt': str(end_date)
                }
            }, {'_id': 0})[0]

            print(stats)

            if stats is None:
                return {}
            else:
                return stats

        except Exception as e:
            print('Error getting day weathers')
            print('Exception:', str(e))

        return {}

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

    def get_weather_for_date(self, start_date, end_date):
        try:
            all_weathers = [format_fo_api(weather) for weather in self.collection.find({
                'vreme': {
                    '$gte': str(start_date),
                    '$lt': str(end_date)
                }
            }, {'_id': 0}).sort('vreme', pymongo.DESCENDING)]

            if all_weathers is not None and len(all_weathers) > 0:
                return all_weathers

            return {}

        except:
            print('Error getting all weathers after {}'.format(str(start_date)))

        return {}

    def get_n_weathers_after(self, date, number, sort_order=pymongo.DESCENDING):
        return self.get_all_weathers_after(date, sort_order)[:number]


    def get_weather_by_id(self, id):
        return self.collection.find_one({
            '_id': ObjectId(id)
        }, {'_id': 0})
