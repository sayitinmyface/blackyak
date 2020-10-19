from django.shortcuts import render
import folium
from pymongo import MongoClient
import geocoder
# Create your views here.
# 지도에 산 모든 위치 표시 
def home(req):
    # 처음 전체 화면 lat,lon
    lat_lon = [36.0040,128.1540]
    m = folium.Map(location=lat_lon,zoom_start=7,tiles='Stamen Terrain')
    #산 정보 get
    list_info = getInfo('mountain_info') 
    # 
    for f_info in list_info:
        lat_lon = [float(f_info['lat']),float(f_info['lon'])]
        weather = getWeatherinfo(float(f_info['lat']),float(f_info['lon']))        
        html = f'''
                    <table border="1" sty>
                        <tr>
                            <td colspan="2"> <img src={f_info["img_path"]} widht="200" height="200"></td>
                            <td>
                                <tr align="center">
                                    <td>WEATHER</td><td>CELSIUS</td>
                                </tr>
                                <tr style="font-style: italic;">
                                    <td align="center">
                                        <img src="{weather['icon_url']}">
                                    </td>
                                    <td align="center">
                                        MAX : {weather['temperature']['temp_max']}<br> MIN : {weather['temperature']['temp_min']}
                                    </td>
                                </tr>
                            </td>
                        </tr>
                    </table>
            '''
        toolhtml = f'<img src={f_info["img_path"]} widht="200" height="200"><img src="{weather["icon_url"]}">'            
        pophtml = folium.Html(html,script=True)
        popup = folium.Popup(pophtml,max_width=2650)
        # folium.templates
        html = f'<div style="background-color: aliceblue;"><font size="2">{f_info["mountain_name"]}</font></div>'
        # 
        folium.Marker(location=lat_lon,icon=folium.DivIcon(html=html)).add_to(m)
        folium.Marker(location=lat_lon,popup=popup,tooltip=toolhtml).add_to(m)        
        # 
    # ip = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # ip.connect(('8.8.8.8',0))
    m = m._repr_html_
    return render(req,'yakmap/home.html',{'map':m})

#DB 산 정보 : mountain_info , 
def getInfo(collection_name,db_url='mongodb://192.168.0.179:27017'):
    with MongoClient(db_url) as client:
        result = list(client['mydb'][collection_name].find())
    return result
# DB 날씨 정보 : weather_info ,
def getWeatherinfo(lat,lon,db_url='mongodb://192.168.0.179:27017'):
    with MongoClient(db_url) as client:
        result = list(client['mydb']['weather_info'].find({'lat':lat,'lon':lon}))
    return result[0]

    
    
