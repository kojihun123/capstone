import pandas as pd
import csv
from geopy import distance
import numpy as np

data = pd.read_csv("./지역화폐 가맹점 현황.csv", encoding='euc-kr')

# Haversine 기본 거리 공식을 정의 (죄표로 직선거리 계산)
def haversine(lat1, lon1, lat2, lon2):
    MILES = 3959
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    total_miles = MILES * c
    return total_miles


#200m 범위에 가게들의 정보를 리턴
def ret_location(lat, long):

    find_row = data.loc[haversine(lat, long, data['위도'], data['경도']) <= 0.1553428]
    result = []
    for d in range(0, len(find_row)):
        result.append(dict(find_row.iloc[d]))
    return result