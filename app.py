from flask import Flask, render_template, request
import gmap

app = Flask(__name__)


@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        data = request.form.get('hidden_addr') # 안전하게 가져오려면 get
        a = data.split(',')[0].lstrip("(")
        b = data.split(',')[1].lstrip(" ").rstrip(")")
        loc_data = gmap.ret_location(float(a), float(b))
        return render_template('index.html', mydata=loc_data)

    elif request.method == "GET":
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)