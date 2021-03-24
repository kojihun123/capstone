from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests


driver = webdriver.Chrome('C:\chromedriver.exe')
driver.get(url = "https://m.map.naver.com/")
driver.implicitly_wait(300)

time.sleep(3)
driver.find_element_by_class_name('Nbox_input_text').click()
driver.find_element_by_class_name('Nbox_input_text._search_input').send_keys('주변 맛집')
driver.find_element_by_xpath('//*[@id="ct"]/div[1]/div[1]/form/div/div[2]/div/span[2]/button[2]').click()
# driver.find_element_by_xpath('/html/body/div[5]/a').click()
time.sleep(3)

replys =driver.find_elements_by_xpath('//*[@id="ct"]/div[2]/ul/li')
print(len(replys))

results = []
for index, reply in enumerate(replys):
        name = reply.find_element_by_css_selector('div.item_tit').text
        address =reply.find_element_by_css_selector('div.wrap_item').text.split('\n')[2]
        latitude = address_to_latitude(address)
        longtitude = address_to_longtitude(address)
        results.append((name, address, latitude, longtitude))