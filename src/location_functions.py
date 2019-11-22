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

def getLocation(_lng,_lat):
    '''creates a variable (loc) in geojson format'''
    try:
        loc = {'type':'Point',
            'coordinates':[float(_lng), float(_lat)]}
        return loc
    except:
        pass

def createLocation(lng,lat,coll,i):
    '''creates an attribute (loc) in geojson format for a given collection (coll)'''
    geocode = {"$set": {'location':getLocation(lng,lat)}}
    coll.update_one(i,geocode)
    
def setLocation(coll):
    '''deletes None coordinates of offices and creates a new attribute with the found coordinates'''
    for i in list(coll.find()):
        lng = i["offices"].get("longitude")
        lat = i["offices"].get("latitude")
        coll.delete_one({"offices.longitude": None})
        createLocation(lng,lat,coll,i)
        
def place_request(direction):
    '''requests information to google places API and returns it in json format'''
    if not os.getenv("google"):
        raise ValueError("No API token!")
    else:
        g = geocoder.google(direction,key=os.getenv("google"))
        return g.json
    
def request_json(url):
'''requests to a concrete url and returns the information in json format'''
    res = requests.get(url).json()
    return res["results"]

def getAdress(results):
'''Returns adress atribute for a given dictionary'''
    return results["formatted_address"]

def getPosition(results):
'''Returns longitude and latitude of a given dictionary'''
    lng = results["geometry"]["location"]["lng"]
    lat = results["geometry"]["location"]["lat"]
    return lng,lat

def insertMongo(coll,s,lng,lat):
'''Inserts in Mongo collection (coll) the calculated atributes of location and adresss'''
    coll.insert_one({'location':getLocation(lng,lat),'adress':getAdress(s)})
    
def getRequest(url):
'''Web parsing using Beautiful Soup'''
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    return soup

def checkLocation(collection):
'''Returns a list of the elements in a collection whose coordinates exist'''
    return list(collection.find({"location.coordinates":{"$exists":True}}))