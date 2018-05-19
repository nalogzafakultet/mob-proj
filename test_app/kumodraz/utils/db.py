from pymongo import MongoClient
from .config import *

db = MongoClient(
    host=DB_HOST,
    port=DB_PORT
)