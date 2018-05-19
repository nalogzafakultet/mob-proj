from flask import request, jsonify, render_template, Blueprint
from kumodraz.models import weather
from pprint import pprint as pp

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/', methods=['GET'])
def index():
    weathers = weather.get_all()
    return render_template('index.html', weathers=weathers)


