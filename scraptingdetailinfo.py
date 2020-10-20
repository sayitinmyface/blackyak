from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
from bs4 import BeautifulSoup
import urllib.request
import time

db_url = 'mongodb://192.168.0.179:27017'
url = 'https://varama.tistory.com/538'
# 
img_path = './static/images/'
# 
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url)
driver.maximize_window()
# 
images = driver.find_elements_by_xpath('//img[@filename]')
# 
for image in images:
    img_name = image.get_attribute('filename')
    img_src = image.get_attribute('src')
    mountain_name = image.get_attribute('filename').split('산')[0]+'산'
    with urllib.request.urlopen(img_src) as res , open(img_path+img_name,'wb') as f:
        data = res.read()
        f.write(data)
    #mongo db
    with MongoClient(db_url) as client:
        mydb = client['mydb']
        detail_info = mydb['detail_info']
        data = {
                'mountain_name':mountain_name,
                'img_path':img_path+img_name
        }
        detail_info.insert_one(data)
    # time.sleep(1)
driver.quit()
    
    
