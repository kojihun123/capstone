# 위도와 경도가 표시되는 구글 맵을 활용해 자신의 현재 위치를 파악하기 위한 모듈
# 현재위치에 따라 url이 바뀌는 성질을 이용하여
# 구글 맵 홈페이지에 들어가 자신의 현재 위치를 파악하는 버튼을 누르고 url을 얻어와
# split을 통해 위도와 경도를 얻어낸다.
# 셀레니움으로 자동 크롤링 하는 방식을 채택


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os


def mylocations():

    options = webdriver.ChromeOptions()

    options.binary_location = os.getenv('GOOGLE_CHROME_BIN')

    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(executable_path=str(os.environ.get('CHROME_EXECUTABLE_PATH')), chrome_options=options)

    driver.get(url = "https://www.google.com/maps")
    driver.implicitly_wait(300)


    #웹페이지 로딩으로 인한 오류를 방지하기위한 While + Try-except 문
    while True:
        try:
            driver.find_element_by_css_selector('#widget-mylocation').click()
            time.sleep(2)
            result = driver.current_url
            #위도경도 테스트
            print(result.split('@')[1].split(',')[0:2])
            break

        except:
            print("웹 페이지 로딩")

    #위도와 경도
    latitude = result.split('@')[1].split(',')[0]
    longtitude = result.split('@')[1].split(',')[1]

    driver.close()

    return latitude, longtitude