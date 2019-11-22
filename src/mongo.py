from pymongo import MongoClient

client = MongoClient()

def connectCollection(database, collection):
    '''creates a unique connection to Mongo server and returns the database and the collection'''
    db = client[database]
    coll = db[collection]
    return db, coll