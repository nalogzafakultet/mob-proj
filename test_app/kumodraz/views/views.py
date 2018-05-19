from flask import request, jsonify, render_template, Blueprint, url_for
from kumodraz.models import weather
from datetime import datetime
from pprint import pprint as pp

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/', methods=['GET'])
def index():
    date_q = datetime(2017, 1, 1, 0, 0, 0, 0)
    weathers = weather.get_n_weathers_after(
        date=date_q,
        number=12
    )
    return render_template('index.html', weathers=weathers)


@main_blueprint.route('/more/<idx>')
def more_info(idx):

    current_weather = weather.get_weather_by_id(idx)
    current_weather['img_url'] = get_picture_url(current_weather)
    return render_template('more.html', weather=current_weather)

def get_picture_url(weather):
    return '/static/img/' + weather['description'] + '.png'