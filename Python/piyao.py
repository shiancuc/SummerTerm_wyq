from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import time
import os
import re
import platform
from lxml import etree
from datetime import datetime

main_page_url = 'https://piyao.sina.cn/'
chrome_driver_path = ""


if platform.system()=='Windows':
    chrome_driver_path = "chromedriver.exe"
elif platform.system()=='Linux' or platform.system()=='Darwin':
    chrome_driver_path = "./chromedriver"
else:
    print('Unknown System Type. quit...')


chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options, \
executable_path= chrome_driver_path)

driver.get(main_page_url)
time.sleep(1)

title_list=[]
comment_list=[]

# 获取页面初始高度
js = "return action=document.body.scrollHeight"
height = driver.execute_script(js)

# 将滚动条调整至页面底部
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(5)

#定义初始时间戳（秒）
t1 = int(time.time())

# 重试次数
num=0

while num < 30:
	# 获取当前时间戳（秒）
    t2 = int(time.time())
    # 判断时间初始时间戳和当前时间戳相差是否大于30秒，小于30秒则下拉滚动条
    if t2-t1 < 30:
        new_height = driver.execute_script(js)
        if new_height > height :
            time.sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            # 重置初始页面高度
            height = new_height
            # 重置初始时间戳，重新计时
            t1 = int(time.time())
    num += 1



for i in range(30):
    i=str(i)
    titles = driver.find_elements_by_xpath('//div[@class="zy_day" and position()='+i+']/div[@class="day_date"]/following-sibling::ul//div[@class="left_title"]')
    for t in titles:
        title_list.append(t.text)
    
    comments = driver.find_elements_by_xpath('//div[@class="zy_day" and position()='+i+']/div[@class="day_date"]/following-sibling::ul//div[@class="comment_text"]')
    for t in comments:
        comment_list.append(int(t.text))


result = zip(title_list,comment_list)
results = sorted(result, key=lambda x : x[1], reverse=True)
results = list(results)

print("最近一个月评论数最高的十条新闻：")
for i in range(10):
    print(results[i][0],end = ' ')
    print("评论数：",end = ' ')
    print(results[i][1])

quit()