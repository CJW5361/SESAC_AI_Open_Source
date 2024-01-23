# app.py
from flask import Flask, render_template
import pandas as pd 
# Flask 객체 인스턴스 생성
app = Flask(__name__)

# 데이터 한 번만 기술
# datas = [
#     {'name': '반원', 'lebel': 60, 'point': 360, 'exp': 45000},
#     {'name': '반원2', 'lebel': 2, 'point': 20, 'exp': 200},
#     {'name': '반원3', 'lebel': 3, 'point': 30, 'exp': 300}
# ]

datas=pd.read_csv('data/data.csv')
datas=datas.to_dict(orient='records')

@app.route('/')  # 접속하는 URL
def index():
    return render_template('index.html', datas=datas)

@app.route('/index_table')  # 접속하는 URL
def index_table():
    return render_template('index_table.html', datas=datas)

if __name__ == "__main__":
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app.run(host="127.0.0.1", port="5000", debug=True)
