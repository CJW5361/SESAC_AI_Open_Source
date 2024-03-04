# image_classifier.py
import streamlit as st
from PIL import Image
from keras.models import load_model
import numpy as np
from PIL import ImageOps  # Install pillow instead of PIL
import numpy as np
from dotenv import load_dotenv 
import os
import image_classifier
import chatbot
import cv2
import streamlit as st
import requests 
from time import sleep
import sys
import time
import pyautogui
# def find_nearest_parking_lot(latitude, longitude, api_key):
#     headers = {
#         'Authorization': f'KakaoAK {api_key}'
#     }
#     params = {
#         'category_group_code': 'PK6',  # 공영주차장 코드
#         'x': longitude,
#         'y': latitude,
#         'radius': 2000,  # 검색 반경 설정 (미터 단위)
#         'sort': 'distance'  # 거리순으로 정렬
#     }
    
#     url = "https://dapi.kakao.com/v2/local/search/category.json"
#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         parking_lots = response.json().get('documents')
#         return parking_lots
#     else:
#         return None
    
# Streamlit 애플리케이션 구성
def app():
    st.title("카카오지도")

    # # Kakao API 키
    api_key = ""  # 자신의 Kakao API 키로 대체해주세요.

    # Kakao 지도의 중심 좌표로 서울을 설정
    lat=37.65
    lng=127.05  # 서울의 위도(latitude)와 경도(longitude)

    # Kakao 지도 웹 페이지의 URL
    # kakao_map_url = f"https://map.kakao.com/link/search/공영주차장?,{lat},{lng}"
    kakao_map_url = f"https://map.kakao.com/link/search/공영주차장?"


    # Streamlit의 iframe을 사용하여 외부 웹 페이지 표시
    st.components.v1.iframe(kakao_map_url, width=800, height=600)
    
    
    url = "https://dapi.kakao.com/v2/local/search/keyword.json?"
    query = "수락산디자인서울거리 공영주차장"

    
    
    if st.button("가장 가까운 공영주차장 찾기"):
    
        # "공영주차장" 키워드로 Kakao 지도 API에 요청을 보냅니다.
        response = requests.get( url, params = {'query':query}, headers={'Authorization' : 'KakaoAK ' + api_key } )
        data = response.json()
        print(data)
        if data.get("documents"):
            # 검색 결과 중에서 가장 첫 번째 결과를 선택합니다.
            first_result = data["documents"][0]

            # 선택된 결과의 좌표를 가져옵니다.
            lat, lng = first_result["y"], first_result["x"]

            # Kakao 지도 길찾기 URL을 생성합니다.
            kakao_map_url = f"https://map.kakao.com/link/to/수락산디자인서울거리 공영주차장,{lat},{lng}"

            # Streamlit의 iframe을 사용하여 길찾기 링크를 표시합니다.
            st.components.v1.iframe(kakao_map_url, width=800, height=600)
            x, y=960,900
            pyautogui.moveTo(x, y, duration=1)

            # 마우스를 클릭하여 입력 위치를 활성화합니다.
            pyautogui.click()

            # "수락산역"을 입력합니다. 입력 전에 약간의 딜레이를 주어 활성화되었는지 확인합니다.
            time.sleep(1)
            pyautogui.write('수락산역')
        else:
            st.error("가장 가까운 공영주차장을 찾을 수 없습니다.")

        
    