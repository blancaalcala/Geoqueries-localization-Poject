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

def pointsFunction(C,office_coords,office_info,air_coord,weight):
    '''creates a list of lists containing the ranking information of each possible office
    (office_coords) related to all the collections (C)'''
    principal = []
    air = []
    names = []
    for coord in range(len(office_coords)):
        res=[]
        for c in range(len(C)):
            d = nearestPlaces(C[c],office_coords[coord],weight[c])
            res.append(d)
        principal.append(res)
        names.append(office_info[coord]["address"])
        air.append(getDistance(office_coords[coord][::-1],air_coord))
    return principal,names,air    

def nearestPlaces(collection,selector,weight):
    '''Returns the points of each collection in terms of the distance of any element
    of the collection to each specific office
    Using geoqueries, we obtained the elements of each collection that fulfill the 
    condition indicated in the geoquery'''
    points = 11
    dist=10
    conv_factor = 0.0001572065389467467/100
    x = list()
    while len(list(x))==0 and points>0:
        x = collection.find({"location":
        {"$geoWithin":{"$centerSphere":[selector,conv_factor*dist]}}})
        dist +=10
        points-=1
    return points*weight/4
