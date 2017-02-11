
from pymongo import *
client = MongoClient()

db = client.test_db

collection = db.douban

def mInsert(obj):
    result = collection.insert_many(obj)
    print result