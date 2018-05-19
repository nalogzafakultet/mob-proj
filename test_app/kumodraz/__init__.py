from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from config import *
from .models import Weather

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

db = MongoClient(
    host=DB_HOST,
    port=DB_PORT
)

weather_model = Weather(db)