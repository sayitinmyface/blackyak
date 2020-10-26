from pymongo import MongoClient
import datetime
import pyowm
# 날씨 정보 
db_url = db_url = 'mongodb://192.168.0.109:27017'
owm = pyowm.OWM('5b457f895ab57ef2daac2b9e32db5319')
mgr = owm.weather_manager()
# 
with MongoClient(db_url) as client:    
    client['mydb']['weather_info'].delete_many({})    
    mtinfo = list(client['mydb']['mountain_info'].find())
    for info in mtinfo:
        lat = float(info['lat'])
        lon = float(info['lon'])
        obj = mgr.weather_at_coords(lat,lon)
        data = {
                'lat' : lat,
                'lon' : lon,
                'wind' : obj.weather.wind(),
                'detailed_status' : obj.weather.detailed_status,
                'icon_url' : obj.weather.weather_icon_url(),
                'temperature' : obj.weather.temperature('celsius'),
                'create_time': str(datetime.datetime.now())
        }
        client['mydb']['weather_info'].insert_one(data)
# my = geocoder.ip()
# ip = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# ip.connect(('8.8.8.8',0))




