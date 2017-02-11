
from pymongo import *
client = MongoClient()

db = client.test_db

collection = db.test_collection

def mInsert(obj):
    result = collection.insert_many(obj)
    print result