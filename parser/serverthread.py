import threading, pymongo
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

MSGLEN = 5000
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

DB_HOST = '167.99.39.202'
DB_PORT = 5055

DB_NAME = 'weather_db'
COLLECTION_NAME = 'weathers'
COLLECTION_STATS_DAY = 'stats_day'
COLLECTION_STATS_MONTH = 'stats_month'
COLLECTION_STATS_YEAR = 'stats_year'


def format_object(weather):
    for key in weather:
        if key == 'vreme':
            weather[key] = datetime.strptime(weather[key], DATE_FORMAT)
    return weather

def aggregate_year_stats(stats):

    if len(stats) == 0:
        return None

    sum_min_tmp = 0.0
    sum_max_tmp = 0.0
    sum_min_vlaz = 0.0
    sum_max_vlaz = 0.0
    sum_min_pritisak = 0.0
    sum_max_pritisak = 0.0
    sum_min_osvetljenje = 0.0
    sum_max_osvetljenje = 0.0

    for stat in stats:
        sum_min_tmp += stat['avg_min_tmp']
        sum_max_tmp += stat['avg_max_tmp']
        sum_min_vlaz += stat['avg_min_vlaz']
        sum_max_vlaz += stat['avg_max_vlaz']
        sum_min_pritisak += stat['avg_min_pritisak']
        sum_max_pritisak += stat['avg_max_pritisak']
        sum_min_osvetljenje += stat['avg_min_osvetljenje']
        sum_max_osvetljenje += stat['avg_max_osvetljenje']

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

    return ret

def aggregate_stats(stats):
    if len(stats) == 0:
        return None

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

    return ret

def weather_stats(weathers):

    if len(weathers) == 0:
        return None

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




class ServerThread(threading.Thread):

    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.client = pymongo.MongoClient(host=DB_HOST, port=DB_PORT)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]
        self.latest = self.collection.find().sort('vreme', pymongo.DESCENDING)[0]
        self.collection_stats_day = self.db[COLLECTION_STATS_DAY]
        self.collection_stats_month = self.db[COLLECTION_STATS_MONTH]
        self.collection_stats_year = self.db[COLLECTION_STATS_YEAR]

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def run(self):
        data = self.sock.recv(2048)
        data = data.decode('utf-8').split(',')
        print('Konektovao se klijent')
        print('Data primljena:', data)
        # temp, vlaz, vetar, osv
        obj = {}
        obj['temperatura'] = float(data[0])
        obj['vlaznost'] = float(data[1])
        obj['pritisak'] = float(data[2])
        obj['osvetljenje'] = int(data[3])
        curr_datetime = datetime.now() + timedelta(hours=2)
        obj['vreme'] = str(curr_datetime)

        current_day = curr_datetime.day
        current_month = curr_datetime.month
        current_year = curr_datetime.year

        latest_datetime = datetime.strptime(self.latest['vreme'], DATE_FORMAT)

        latest_day = latest_datetime.day
        latest_month = latest_datetime.month
        latest_year = latest_datetime.year

        if curr_datetime > latest_datetime:
            stats = self.stats_for_day(latest_year, latest_month, latest_day)
            stats['date'] = str(latest_datetime)

            self.collection_stats_day.insert_one(stats)

            if current_month != latest_month:
                stats = self.stats_for_month(latest_year, latest_month)
                stats['date'] = str(latest_datetime)
                self.collection_stats_month.insert_one(stats)

            if current_year != latest_year:
                stats = self.stats_for_year(latest_year)
                stats['date'] = str(latest_datetime)
                self.collection_stats_year.insert_one((stats))

        print('Objekat:', obj)
        str_id = self.collection.insert_one(obj)
        print('Inserted:', str_id)

    def stats_for_day(self, current_year, current_month, current_day):
        start_date = datetime(current_year, current_month, current_day)
        end_date = start_date + timedelta(days=1)

        all_weathers = [weather for weather in self.collection.find({
            'vreme': {
                '$gte': str(start_date),
                '$lt': str(end_date)
            }
        }, {'_id': 0})]

        return weather_stats(all_weathers)

    def stats_for_month(self, current_year, current_month):
        start_date = datetime(current_year, current_month, 1)
        end_date = start_date + relativedelta(months=1)

        all_stats = [stat for stat in self.collection_stats_day.find({
            'date': {
                '$gte': str(start_date),
                '$lt': str(end_date)
            }
        }, {'_id': 0})]

        return aggregate_stats(all_stats)

    def stats_for_year(self, current_year):
        start_date = datetime(current_year, 1, 1)
        end_date = start_date + relativedelta(years=1)

        all_stats = [stat for stat in self.collection_stats_month.find({
            'date': {
                '$gte': str(start_date),
                '$lt': str(end_date)
            }
        }, {'_id': 0})]

        return aggregate_year_stats(all_stats)

