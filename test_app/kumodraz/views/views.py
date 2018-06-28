from flask import request, jsonify, render_template, Blueprint, url_for
from kumodraz.models import weather
from datetime import datetime
from datetime import timedelta
from pprint import pprint as pp
from dateutil.relativedelta import relativedelta

from kumodraz.utils.config import DATE_FORMAT, DAY_FORMAT

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/', methods=['GET'])
def index():
    date_q = datetime(2017, 1, 1, 0, 0, 0, 0)

    weathers = weather.get_all()
    return render_template('index.html', weathers=weathers)


@main_blueprint.route('/more/<idx>')
def more_info(idx):

    current_weather = weather.get_weather_by_id(idx)
    return render_template('more.html', weather=current_weather)

@main_blueprint.route('/api/test/month')
def get_test_stats():
    dan = request.args.get('datum')

    if dan is None:
        return {}
    else:
        start_date = datetime.strptime(dan, DAY_FORMAT)
        
        month = start_date.month
        year = start_date.year

        print('Month: {}, Year: {}'.format(month, year))

        return jsonify(weather.stats_per_month(month, year))

        # return jsonify(weather.get_weather_for_date(start_date, end_date))


@main_blueprint.route('/api/weathers/day')
def get_weathers_day():
    dan = request.args.get('datum')

    print(dan)

    if dan is None:
        return {}
    else:
        start_date = datetime.strptime(dan, DAY_FORMAT)
        end_date = start_date + timedelta(days=1)

        return jsonify(weather.get_weather_for_date(start_date, end_date))

@main_blueprint.route('/api/weathers/month')
def get_weathers_month():
    dan = request.args.get('datum')

    print(dan)

    if dan is None:
        return {}
    else:
        start_date = datetime.strptime(dan, DAY_FORMAT)
        end_date = start_date + relativedelta(months=1)

        return jsonify(weather.get_weather_for_date(start_date, end_date))

@main_blueprint.route('/api/weathers/year')
def get_weathers_year():
    dan = request.args.get('datum')

    print(dan)

    if dan is None:
        return {}
    else:
        start_date = datetime.strptime(dan, DAY_FORMAT)
        end_date = start_date + relativedelta(years=1)

        return jsonify(weather.get_weather_for_date(start_date, end_date))

@main_blueprint.route('/api/now')
def get_last_weather():
    return jsonify(weather.get_last())

@main_blueprint.route('/api/stats/year')
def get_stats_year():
    dan = request.args.get('datum')

    print(dan)

    if dan is None:
        return {}
    else:
        start_date = datetime.strptime(dan, DAY_FORMAT)
        end_date = start_date + relativedelta(years=1)

        return jsonify(weather.get_stats_for_year(start_date, end_date))

@main_blueprint.route('/api/stats/day')
def get_stats_day():
    dan = request.args.get('datum')

    print(dan)

    if dan is None:
        return {}
    else:
        start_date = datetime.strptime(dan, DAY_FORMAT)
        end_date = start_date + relativedelta(days=1)

        return jsonify(weather.get_stats_for_day(start_date, end_date))

@main_blueprint.route('/api/stats/month')
def get_stats_month():
    dan = request.args.get('datum')

    print(dan)

    if dan is None:
        return {}
    else:
        start_date = datetime.strptime(dan, DAY_FORMAT)
        end_date = start_date + relativedelta(months=1)

        return jsonify(weather.get_stats_for_month(start_date, end_date))

@main_blueprint.route('/api/recent/day')
def get_recent_day():

    now = datetime.now()
    yday = now - timedelta(hours=24)

    print('NOW: {}, YDAY: {}'.format(str(now), str(yday)))

    return jsonify(weather.get_weather_for_date(yday, now))

@main_blueprint.route('/api/newrecent/day')
def get_new_recent_day():
    return jsonify(weather.get_recent_weather(hours=24))

@main_blueprint.route('/api/recent/threedays')
def get_recent_threedays():

    now = datetime.now()
    yday = now - relativedelta(hours=72)

    return jsonify(weather.get_weather_for_date(yday, now))

@main_blueprint.route('/api/recent/week')
def get_recent_week():

    now = datetime.now()
    yday = now - relativedelta(hours=168)

    return jsonify(weather.get_weather_for_date(yday, now))

@main_blueprint.route('/api/recent/month')
def get_recent_month():

    now = datetime.now()
    today = datetime(now.year, now.month, now.day)
    start = today - relativedelta(days=30)

    print('START: {}, END: {}'.format(start, today))

    return jsonify(weather.get_new_stats_for_month(start, today))

@main_blueprint.route('/api/newstats/year')
def newstats_year():
    year = request.args.get('year')
    return jsonify(weather.new_stats_for_year(year))

@main_blueprint.route('/api/newstats/month')
def newstats_month():
    year = request.args.get('year')
    month = request.args.get('month')
    return jsonify(weather.new_stats_for_month(year, month))


@main_blueprint.route('/api/getall')
def get_all():
    return "asdsa"

def get_picture_url(weather):
    return '/static/img/' + weather['description'] + '.png'
