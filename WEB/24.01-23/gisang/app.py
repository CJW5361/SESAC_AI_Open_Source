import pandas as pd 
url='https://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList?serviceKey=wKXVoZD3JTnajz7I2NG5STcdGGkG%2B9wYeT0RnnZnbFzOnVpgdv5oysBgCVdD3HomSPkHinfymX9QAYSjj2Vc1Q%3D%3D&pageNo=1&numOfRows=152&dataType=XML&dataCd=ASOS&dateCd=DAY&startDt=20100101&endDt=20100601&stnIds=108'
datas=pd.read_html(url,encoding='utf-8')

datas=datas.to_dict(orient="records")
datas
