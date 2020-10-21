from django.shortcuts import render
import folium
from pymongo import MongoClient
import geocoder
# from ipyleaflet import *
# Create your views here.
# 지도에 산 모든 위치 표시 
def index(req):
    # print('start')
    # 처음 전체 화면 lat,lon
    lat_lon = [36.0040,128.1540]
    m = folium.Map(location=lat_lon,zoom_start=6,tiles='Stamen Terrain')    
    # m.get_root().add_child(folium.JavascriptLink('./static/js/test.js'))
    #산 정보 get
    list_info = getInfo('mountain_info') 
    list_visitname = list(set([name['visitName'] for name in list_info]))
    list_visitname.sort()
    # 
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
        folium.Marker(location=lat_lon,icon=folium.DivIcon(html=html)).add_to(m)
        folium.Marker(location=lat_lon,popup=popup,tooltip=toolhtml).add_to(m)        
        #         
    m = m._repr_html_
    # 상세 정보 
    # list_detail = getInfo('detail_info')
    data = {'map':m,'list_visitname':list_visitname,'list_info':list_info}
    # return render(req,'yakmap/home.html',{'map':m})
    return render(req,'index.html',data)
# 
def local(req):
    
    return render(req,'index.html')

#DB 산 정보 : mountain_info , 상세 정보사진 : detail_info
def getInfo(collection_name,local_name='',db_url='mongodb://192.168.0.179:27017'):
    with MongoClient(db_url) as client:
        # 산 정보
        # if collection_name == 'mountain_info':
            # result = list(client['mydb'][collection_name].find({'visitName':{'$ne':''}}))
        result = list(client['mydb'][collection_name].find())
        # 산 상세 정보사진
        # if collection_name == 'detail_info' and local_name == '':
        #     result = list(client['mydb'][collection_name].find())
        # else:
        #     result = list(client['mydb'][collection_name].find({'mountain_name':local_name}))
    return result
# DB 날씨 정보 : weather_info ,
def getWeatherinfo(lat,lon,db_url='mongodb://192.168.0.179:27017'):
    with MongoClient(db_url) as client:
        result = list(client['mydb']['weather_info'].find({'lat':lat,'lon':lon}))
    return result[0]

    
    
