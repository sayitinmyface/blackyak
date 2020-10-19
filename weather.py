from pymongo import MongoClient
import datetime
import pyowm
import datetime
# 날씨 정보 
db_url = db_url = 'mongodb://192.168.0.179:27017'
owm = pyowm.OWM('5b457f895ab57ef2daac2b9e32db5319')
mgr = owm.weather_manager()
# 
with MongoClient(db_url) as client:    
    mtinfo = list(client['mydb']['mountain_info'].find())
    for info in mtinfo:
        lat = float(info['lat'])
        lon = float(info['lon'])
        obj = mgr.weather_at_coords(lat,lon)
        data = {
                'lat' : lat,
                'lon' : lon,
                'icon_url' : obj.weather.weather_icon_url(),
                'temperature' : obj.weather.temperature('celsius'),
                'create_time': str(datetime.datetime.now())
        }
        client['mydb']['weather_info'].insert_one(data)




