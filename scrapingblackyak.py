from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import datetime
from bs4 import BeautifulSoup
import urllib.request

db_url = 'mongodb://192.168.219.105:27017'
url = 'http://bac.blackyak.com/html/challenge/ChallengeVisitList.asp?CaProgram_key=114'
# 
img_path = './static/images/'
# 
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get(url)
driver.maximize_window()
# 
div = driver.find_element_by_class_name('searchList')
li = div.find_elements_by_tag_name('li')
# 
# 
for f_li in li:
    mountain_name = f_li.find_element_by_tag_name('span').text
    # 위도 경도
    lat,lon = tuple(f_li.find_element_by_tag_name('a').text.split(','))
    # 상세보기 클릭
    f_li.find_element_by_tag_name('button').click()
    # 새탭
    driver.switch_to_window(driver.window_handles[-1])
    # bs4
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    # 상세설명
    visitText = soup.select_one('p.visitText').string
    # 이미지 저장
    img_src = driver.find_element(By.XPATH,'//div[@class="img"]/img').get_attribute('src')
    image_name = mountain_name+'.'+img_src.split('.')[-1]
    with urllib.request.urlopen(img_src) as res , open(img_path+image_name,'wb') as f:
        data = res.read()
        f.write(data)
    #mongo db
    with MongoClient(db_url) as client:
        mydb = client['mydb']
        mountain_info = mydb['mountain_info']
        data = {
                'mountain_name':mountain_name,
                'lat':lat,
                'lon':lon,
                'visitText':visitText,
                'img_path':img_path+image_name,
        }
        mountain_info.insert_one(data)
    print()
