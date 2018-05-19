from flask import request, jsonify, render_template, Blueprint
from kumodraz.models import weather

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/', methods=['GET'])
def index():
	return render_template('index.html')


