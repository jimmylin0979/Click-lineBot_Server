from sqlite3.dbapi2 import connect
from typing import List
import requests
import polyline
import folium
import sqlite3
import pandas as pd

class AEDMap:

    def __init__(self) -> None:
        # Variable Initialization
        self.fmap = None

        # DataBase filePath & Open the connection
        DB_Name = 'AED.db'
        conn = sqlite3.connect(DB_Name)

    def route(self, frm, des, mode="foot"):
        '''

        '''

        # frm, des should be a list of lat & log : [lat, log], ex :
        # frm = [33.698116, -117.851235]
        # des = [33.672133, -117.838617]
        
        # GET
        url = f"http://router.project-osrm.org/route/v1/{mode}/{frm[1]},{frm[0]};{des[1]},{des[0]}"
        r = requests.get(url)

        # UnSerialization
        res = r.json()

        return res

    def get_map(self, frm, des, mode="foot"):
        
        # route 
        res = self.route(frm, des, mode=mode)

        # decode the wayPoints via Polyline Algo
        wayPoints = polyline.decode(res['routes'][0]['geometry'])

        # packing the variable
        route = {'route': wayPoints,
        'start_point': frm,
        'end_point': des,
        'distance': res['routes'][0]['distance']}

        # drawing the folium map
        self.fmap = folium.Map(location=[(route['start_point'][0] + route['end_point'][0])/2, 
                                (route['start_point'][1] + route['end_point'][1])/2], 
                    zoom_start=13)

        folium.PolyLine(
            route['route'],
            weight=8,
            color='blue',
            opacity=0.6
        ).add_to(self.fmap)

        folium.Marker(
            location=route['start_point'],
            icon=folium.Icon(icon='play', color='green')
        ).add_to(self.fmap)

        folium.Marker(
            location=route['end_point'],
            icon=folium.Icon(icon='stop', color='red')
        ).add_to(self.fmap)

        # and return html code
        return self.fmap._repr_html_()
    
    def toFlask(self):
        return self.fmap._repr_html()

    def save(self, fileName='AEDMap.html'):
        self.fmap.save(fileName)