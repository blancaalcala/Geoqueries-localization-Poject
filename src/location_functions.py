import os
import re
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from bs4 import BeautifulSoup
import geocoder
import requests
import folium
from folium.plugins import MousePosition
from folium.plugins import Draw
from geopy.distance import distance as getDistance
load_dotenv()


def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

def getLocation(_lng,_lat):
    try:
        loc = {'type':'Point',
            'coordinates':[float(_lng), float(_lat)]}
        return loc
    except:
        pass

def createLocation(lng,lat,coll,i):
    geocode = {"$set": {'location':getLocation(lng,lat)}}
    coll.update_one(i,geocode)
    
def setLocation(coll):
    for i in list(coll.find()):
        lng = i["offices"].get("longitude")
        lat = i["offices"].get("latitude")
        coll.delete_one({"offices.longitude": None})
        createLocation(lng,lat,coll,i)
        
def place_request(direction):
    if not os.getenv("google"):
        raise ValueError("No API token!")
    else:
        g = geocoder.google(direction,key=os.getenv("google"))
        return g.json
    
def request_json(url):
    res = requests.get(url).json()
    return res["results"]

def getAdress(results):
    return results["formatted_address"]

def getPosition(results):
    lng = results["geometry"]["location"]["lng"]
    lat = results["geometry"]["location"]["lat"]
    return lng,lat

def insertMongo(coll,s,lng,lat):
    coll.insert_one({'location':getLocation(lng,lat),'adress':getAdress(s)})
    
def getRequest(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    return soup

def checkLocation(collection):
    return list(collection.find({"location.coordinates":{"$exists":True}}))