from flask import Flask, render_template, request
import current_loaction

app = Flask(__name__)


@app.route('/')
def index():
    
    #보낼 현제 위치 데이터 (위도, 경도)
    value = current_loaction.mylocation()

    data = {'위도':value[0], '경도':value[1]}


    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
