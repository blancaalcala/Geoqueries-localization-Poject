from pymongo import MongoClient

client = MongoClient()

def connectCollection(database, collection):
    db = client[database]
    coll = db[collection]
    return db, coll