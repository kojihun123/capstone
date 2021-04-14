import pandas as pd
import csv
from geopy import distance
import numpy as np

data = pd.read_csv("./지역화폐 가맹점 현황.csv", encoding='euc-kr')

test = '일반휴게음식|음료식품'

# a = data[data['업종명(종목명)'].str.contains(test, na=False) == False]
a = data[data['업종명(종목명)'].str.contains(test, na=False)]

pd.set_option('display.max_rows', None)
print(a['업종명(종목명)'])



#일반휴게음식, 음료식품, 보건위생, 문화.취미, 의류, 약국, 레져용품, 서적문구, 주방용구, 학원,
#자동차정비 유지, 용역 서비스, 가구, 수리서비스, 건축자재, 직물, 의원, 신변잡화, 여행, 레저업소
#회원제형태, 기타, 사무통신, 유통업(편의점이나 마트) 영리, 농업, 건강식품, 광학제품, 전기제품, 연료판매점,
#자동차판매, 별도관리, 숙박업, 병원, GS25, 보험, 음식점(다방,치킨,), 서비스업(스크린골프), 음식점업, 스포츠