# app.py
from flask import Flask, render_template
import pandas as pd 
# Flask 객체 인스턴스 생성
app = Flask(__name__)


import pandas as pd 
url='http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=005930'
datas=pd.read_html(url,encoding='utf-8')[12]
datas=datas.to_dict(orient="records")
datas

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
