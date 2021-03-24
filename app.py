from flask import Flask, render_template, request
import current_loaction

app = Flask(__name__)


@app.route('/')
def index():
    
    #보낼 현제 위치 데이터 (위도, 경도)
    #value1, value2 = current_loaction.mylocations()
    #data1=value1, data2=value2
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
