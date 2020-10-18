from django.shortcuts import render
import folium
from pymongo import MongoClient
import pyowm
# Create your views here.
# 지도에 산 모든 위치 표시 
def home(req):
    # 처음 전체 화면 lat,lon
    lat_lon = [36.0040,128.1540]
    m = folium.Map(location=lat_lon,zoom_start=7,tiles='Stamen Terrain')
    # 날씨 정보
    owm = pyowm.OWM('5b457f895ab57ef2daac2b9e32db5319')#api key value
    mgr = owm.weather_manager()
    #산 정보 get
    list_info = getInfo('mountain_info') 
    # 
    for f_info in list_info:
        lat_lon = [float(f_info['lat']),float(f_info['lon'])]
        # obj = mgr.weather_at_coords(float(f_info['lat']),float(f_info['lon']))
        # w = obj.weather
        html = f'''
                    <table border="1">
                        <tr>
                            <td colspan="2"> <img src={f_info["img_path"]}></td>
                        </tr>
                        <tr>
                            <td>

                            </td>
                        </tr>
                    </table>
            '''
        pophtml = folium.Html(html,script=True)
        popup = folium.Popup(pophtml,max_width=2650)
        html = f'<div style="background-color: aliceblue;"><font size="2">{f_info["mountain_name"]}</font></div>'
        # 
        folium.Marker(location=lat_lon,icon=folium.DivIcon(html=html)).add_to(m)
        folium.Marker(location=lat_lon,popup=popup).add_to(m)        
    # 
    m = m._repr_html_
    return render(req,'yakmap/home.html',{'map':m})

#DB find 
def getInfo(collection_name):
    db_url = db_url = 'mongodb://192.168.219.105:27017'
    with MongoClient(db_url) as client:
        result = list(client['mydb'][collection_name].find())
    return result
# 

    
    
