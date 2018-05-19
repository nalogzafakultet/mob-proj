from flask import request, jsonify, render_template, Blueprint
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


