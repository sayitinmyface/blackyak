from django.shortcuts import render
import folium
from pymongo import MongoClient
# Create your views here.
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
# 
def getInfo(collection_name):
    db_url = db_url = 'mongodb://192.168.219.105:27017'
    with MongoClient(db_url) as client:
        result = list(client['mydb'][collection_name].find())
    return result
# 
def showmap(req):
    lat_lon = [36.0040,128.1540]
    # m = folium.Map(zoom_start=7.5)
    m = folium.Map(location=lat_lon,zoom_start=7)
    pophtml = folium.Html('<img src="./static/images/test.jpeg"><b>Jirisan</b>',script=True)
    popup = folium.Popup(pophtml,max_width=2650)
    # folium.CircleMarker(popup=popup,radius=15,fill=True,fill_color='blue',color='red').add_to(m)
    # folium.CircleMarker(location=lat_lon,popup=popup,radius=15,fill=True,fill_color='blue',color='red').add_to(m)
    m = m._repr_html_
    return render(req,'maps/showmap.html',context={'map':m})