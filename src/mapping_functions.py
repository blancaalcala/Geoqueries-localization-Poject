import os
import re
import pandas as pd
from dotenv import load_dotenv
import location_functions as L
from pymongo import MongoClient
from bs4 import BeautifulSoup
import geocoder
import requests
import folium
from folium.plugins import MousePosition
from folium.plugins import Draw
from geopy.distance import distance as getDistance
from IPython.display import HTML
load_dotenv()

def mapResults(centre,zoom,names,colors,collections,air_coord,office_coords,name):

    m = folium.Map(centre, zoom_start=zoom,tiles='cartodbpositron')

    school_group = folium.FeatureGroup(name=names[0]).add_to(m)
    start_group = folium.FeatureGroup(name=names[1]).add_to(m)
    old_comp_group = folium.FeatureGroup(name=names[2]).add_to(m)
    starbucks_group = folium.FeatureGroup(name=names[3]).add_to(m) 
    night_group = folium.FeatureGroup(name=names[4]).add_to(m)
    vegan_group = folium.FeatureGroup(name=names[4]).add_to(m)
    plane_group = folium.FeatureGroup(name=names[5]).add_to(m)
    office_group = folium.FeatureGroup(name=names[6]).add_to(m)
    groups = [school_group,start_group,old_comp_group,starbucks_group,night_group,vegan_group,plane_group,office_group]

    for g in range(len(groups)-2):
        for c in L.checkLocation(collections[g]):
            coord = c["location"]["coordinates"][::-1]
            icon=folium.Icon(color=colors[g])
            groups[g].add_child(folium.Marker(coord,popup=names[g]+" "+str(coord),icon=icon))   

    icon=folium.Icon(icon='cloud',color='lightblue', prefix='Airport')
    plane_group.add_child(folium.Marker(air_coord,popup="Airport "+str(air_coord),icon=icon))
    
    if len(office_coords)>2:
        for o in office_coords:
            icon=folium.Icon(color='darkblue')
            office_group.add_child(folium.Marker(o[::-1],popup=names[g]+" "+str(coord),icon=icon))   
    else:
        icon=folium.Icon(color='darkblue')
        office_group.add_child(folium.Marker(office_coords,popup="CHOSEN OFFICE"+" "+str(coord),icon=icon)) 

    folium.LayerControl(collapsed=True).add_to(m)
    folium.LatLngPopup().add_to(m)
    draw = Draw(export=True)
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    MousePosition(
        position='topright',
        separator=' | ',
        lng_first=True,
        prefix='Coordinates:',
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)
    draw.add_to(m)
    m.save(f'../output/{name}.html')
    
def mappingChoice():
    continue_map = bool(input("Do you want to see a map? (press enter to exit)"))
    while continue_map:
        map_name = input("Which map do you want to see? (initial_map / final_map): ")
        display(HTML(f'<iframe src=../output/{map_name}.html width=700 height=450></iframe>'))
        continue_map = bool(input("Do you want to see another map? (press enter to exit)"))