from django.shortcuts import render
import folium
from pymongo import MongoClient
import geocoder
from django.core.paginator import Paginator
# from ipyleaflet import *
# Create your views here.

# 지도에 산 모든 위치 표시 
def maping(map_info,list_info):
    # map 정보
    for f_info in list_info:
        lat_lon = [float(f_info['lat']),float(f_info['lon'])]
        #날씨 정보
        weather = getWeatherinfo(float(f_info['lat']),float(f_info['lon']))        
        html = f'''                  
                    <table border="1">
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
        toolhtml = f'<img src={f_info["img_path"]} widht="200" height="200">'            
        pophtml = folium.Html(html,script=True)
        popup = folium.Popup(pophtml,max_width=2650)
        mt_name = f_info["mountain_name"].split('산')[0]+'산'
        html = f'<div style="background-color: aliceblue;"><font size="2">{mt_name}</font></div>'
        # 
        folium.Marker(location=lat_lon,icon=folium.DivIcon(html=html)).add_to(map_info)
        folium.Marker(location=lat_lon,popup=popup,tooltip=toolhtml).add_to(map_info)        
        #         
    m = map_info._repr_html_
    return m
# 
def index(req):
    # 처음 전체 화면 lat,lon    
    lat_lon = [36.0040,128.1540]
    list_info = getInfo('mountain_info') 
    # 
    m = folium.Map(location=lat_lon,zoom_start=7,tiles='Stamen Terrain')    
    #산 정보 get    
    list_visitname = list(set([name['visitName'] for name in list_info]))
    list_visitname.sort()
    # 산 정보 지도에 표시
    m = maping(m,list_info)
    # 상세 정보 
    # list_detail = getInfo('detail_info')
    data = {'map':m,'list_visitname':list_visitname,'list_info':list_info}
    return render(req,'index.html',data)

# 지역 산 정보
def local(req,local_name):
    lat_lon = getInfo('local_latlon')[0][local_name]
    list_info = getInfo('mountain_info') 
    list_info_mt = getdetailinfo('mountain_info','visitName',local_name) 
    # 
    m = folium.Map(location=lat_lon,zoom_start=8,tiles='Stamen Terrain')    
    #산 정보 get    
    list_visitname = list(set([name['visitName'] for name in list_info]))
    list_visitname.sort()
    # 산 정보 지도에 표시
    m = maping(m,list_info_mt)
    # 상세 정보 
    data = {
            'map':m,
            'list_visitname':list_visitname,
            'list_info':list_info,
            'list_info_mt':list_info_mt,
            'lat':lat_lon[0],
            'lon':lat_lon[1]
        }
    return render(req,'yakmap/local.html',data)

#DB 산 정보 : mountain_info , 상세 정보사진 : detail_info , 각 도 중앙 위도,경도 : local_latlon
def getInfo(collection_name,db_url='mongodb://192.168.0.179:27017'):
    # 모든 정보 
    with MongoClient(db_url) as client:
        result = list(client['mydb'][collection_name].find())
    return result

#DB 산 정보 : mountain_info , 상세 정보사진 : detail_info , 각 도 중앙 위도,경도 : local_latlon    
def getdetailinfo(collection_name,col_name,value,db_url='mongodb://192.168.0.179:27017'):
    # 상제 정보
    with MongoClient(db_url) as client:
        result = list(client['mydb'][collection_name].find({col_name:value}))
    return result

# DB 날씨 정보 : weather_info ,
def getWeatherinfo(lat,lon,db_url='mongodb://192.168.0.179:27017'):
    with MongoClient(db_url) as client:
        result = list(client['mydb']['weather_info'].find({'lat':lat,'lon':lon}))
    return result[0]

    
    
