from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests
import urllib.parse
import time
import json
import pytz
import re
import random
from time import sleep
import os
import json
import ast
from datetime import date
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup,Comment




def business_today():
    print('Processing BusinessToday Started ')
    url = f'https://www.businesstoday.in/api/loadmoredata?apiRoute=groupsearchlist%3Fq%3Dtop%2520stocks%2520to%2520watch%26lang%3Den%26site%3Dbt%26ctype%3Dall%26rtype%3Dundefined%26datestart%3D%26dateend%3D%26daterange%3D%26sr%3Dcreateddatetime%26sro%3Ddescsize%3D10%26template%3Doutput_bt_company&size=10&isFrom=true&from=0'
    response = requests.get(url, headers={'Accept':'application/json'})
        # for i in response.json()['data']['content']:
    i = response.json()['data']['content'][0]
    # print(f"BUSINESS-TODAY > i['datetime_published'],i['title_short'],i['share_link_url']")
    return (i['title_short'],i['share_link_url'])
ab=business_today()
print(ab)
 

options=Options()
options.add_experimental_option("detach",True)
driver=webdriver.Chrome(options=options)

# driver.get("https://www.businesstoday.in/markets/stocks/story/top-stocks-in-news-maruti-suzuki-mcx-voda-idea-auro-pharma-nmdc-railtel-509049-2026-01-02")

driver.get(ab[1])
wait=WebDriverWait(driver,10)

main=wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"content_area")))
print(len(main))

unique=set()
for data in main:
    content=data.find_elements(By.CSS_SELECTOR,".text-formatted.field p,h1,h2")
    # print(content)
    
    for i in content:
        driver.execute_script("arguments[0].scrollIntoView();", i)
        time.sleep(0.2)

        text = i.get_attribute("innerText").strip()
        
        if text and text not in unique:
            unique.add(text)
            print(text)
driver.quit()