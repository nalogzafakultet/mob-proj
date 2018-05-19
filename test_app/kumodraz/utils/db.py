from pymongo import MongoClient
from .config import *
from instance.params import *

client = MongoClient(
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USERNAME,
    password=DB_SECRET
)

db = client[DB_DATABASE_NAME]