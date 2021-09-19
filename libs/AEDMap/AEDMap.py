import requests
import polyline
import folium
import sqlite3
import pandas as pd

class AEDInfo:
    def __init__(self, frm, idx, name, pos, tele) -> None:
        # START POSITION (USER LOCATION)
        self.frm = frm         # List[LAT, LNG] : 起點位置 經緯度
        
        # AED INFO
        self.idx = idx
        self.name = name
        self.pos = pos         # List[LAT, LNG] : AED位置 經緯度
        self.tele = tele        

        # DISTANCE (BETWEEN USER AND AED)
        self.distance = self.getDistance()   # 距離

    def getDistance(self) -> float:
        
        # Choose the method of getting distance 
        GET_DISTANCE_METHOD = 0

        if GET_DISTANCE_METHOD == 0:

            # 1. 進行 frm, pos 點對點 三角函示取距離 (畢達哥拉斯三角形)
            # 簡單快速 但 不夠精確
            dis_in_power2 = (self.frm[0] - self.pos[0]) ** 2 + (self.frm[1] - self.pos[1]) ** 2
            return dis_in_power2 ** 0.5

        elif GET_DISTANCE_METHOD == 1:
            # 2. 以 OSRM 取得實際行走距離
            # 花費時間多 但 絕對更精確

            # TODO : 花費時間過多，無法做到即時反應 
            # BUG : 
            # GET
            url = f"http://router.project-osrm.org/route/v1/foot/{self.frm[1]},{self.frm[0]};{self.pos[1]},{self.pos[0]}"
            r = requests.get(url)

            # UnSerialization
            res = r.json()
            return res['routes'][0]['distance']

    def __lt__(self, other):
        return self.distance < other.distance
    def __repr__(self):
        return f"起點={self.frm},距離={self.distance},資訊=[{self.idx},{self.name},{self.pos},{self.tele}]\n"
        # return "AEDInfo()"
    def __str__(self):
        return f"起點={self.frm},距離={self.distance},資訊=[{self.idx},{self.name},{self.pos},{self.tele}]\n"

class AEDMap:

#########################################################################################
# CONSTRUCTOR
    def __init__(self) -> None:
        # Variable Initialization
        self.fmap = None

        # DataBase filePath & Open the connection
        DB_Name = 'AED.db'
        self.conn = sqlite3.connect(DB_Name)

#########################################################################################
# PRIVATE 
    
    def route(self, frm, des, mode="foot"):
        '''

        '''

        # frm, des should be a list of lat & lng : [lat, lng], ex :
        # frm = [33.698116, -117.851235]
        # des = [33.672133, -117.838617]
        
        # GET
        url = f"http://router.project-osrm.org/route/v1/{mode}/{frm[1]},{frm[0]};{des[1]},{des[0]}"
        r = requests.get(url)

        # UnSerialization
        res = r.json()

        return res

    def get_Neary_AEDLocation(self, pos):
        '''

        '''
        # set the AED Searching Radius
        # the larger the radius is, the more time it executes 
        LAT_RADIUS = 0.5
        LNG_RADIUS = 0.5

        # create cursor and do SQL command
        cur = self.conn.cursor()
        cur.execute(f'''
            SELECT * FROM AED
            WHERE {pos[0] - LAT_RADIUS} <= LAT AND LAT <= {pos[0] + LAT_RADIUS}   
                AND {pos[1] - LNG_RADIUS} <= LNG AND LNG <= {pos[1] + LNG_RADIUS};
        ''')

        # fetch row data
        AED_Nearby_Locations = []
        rows = cur.fetchall()
        for row in rows:
            cur = AEDInfo(pos, row[0], row[1], [row[2], row[3]], row[4])
            AED_Nearby_Locations.append(cur)

        # sort the AED_Nearby_Locations by distance
        # the shortest distance, the former it should be in the list
        AED_Nearby_Locations.sort()

        return AED_Nearby_Locations

#########################################################################################
# PUBLIC 

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

    def save(self, fileName='AEDMap.html'):
        self.fmap.save(fileName)

#########################################################################################

if __name__ == "__main__":
    # DEBUG USE ONLY
    fmap = AEDMap()
    AED_Nearby_Locations = fmap.get_Neary_AEDLocation([22.698116, 120.851235])
    print(AED_Nearby_Locations)