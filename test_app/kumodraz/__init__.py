from flask import Flask, jsonify
from pymongo import MongoClient
from config import *
from .models import Weather

app = Flask(__name__)

db = MongoClient(
    host=DB_HOST,
    port=DB_PORT
)

weather_model = Weather(db)