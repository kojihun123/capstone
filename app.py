from flask import Flask, render_template, request
import current_loaction

app = Flask(__name__)


@app.route('/')
def index():
    
    #보낼 현제 위치 데이터 (위도, 경도)
    value = current_loaction.mylocation()

    return render_template('index.html', data1=value[0], data2=value[1])

if __name__ == '__main__':
    app.run(debug=True)
