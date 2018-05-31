from pymongo import MongoClient
from .config import *

client = MongoClient(
    host=DB_HOST,
    port=DB_PORT,
)

db = client[DB_DATABASE_NAME]