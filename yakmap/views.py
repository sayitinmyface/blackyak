from django.shortcuts import render
import folium
from pymongo import MongoClient
# Create your views here.
# 지도에 산 모든 위치 표시 
def home(req):
    lat_lon = [36.0040,128.1540]
    m = folium.Map(location=lat_lon,zoom_start=7)
    # 
    list_info = getInfo('mountain_info')    
    # 
    for f_info in list_info:
        lat_lon = [float(f_info['lat']),float(f_info['lon'])]
        folium.RegularPolygonMarker(location=lat_lon).add_to(m)
    # 
    m = m._repr_html_
    # 
    return render(req,'yakmap/home.html',{'map':m})

# 산 정보 
def getInfo(collection_name):
    db_url = db_url = 'mongodb://192.168.219.105:27017'
    with MongoClient(db_url) as client:
        result = list(client['mydb'][collection_name].find())
    return result
# 
