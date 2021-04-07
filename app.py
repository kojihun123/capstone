from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        data = request.form.get('hidden_addr') # 안전하게 가져오려면 get
        print(data)

        return render_template('index.html')

    elif request.method == "GET":
        user = "반원"
        data = {'level': 60, 'point': 360, 'exp': 45000}
        return render_template('index.html')


if __name__ == '__main__':
    app.run()