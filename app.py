from flask import Flask, render_template, jsonify, request
import gmap

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ajax', methods=['POST'])
def ajax():
    data = request.get_json()
    print(type(data))

    return jsonify(result = "success", result2= data)


if __name__ == '__main__':
    app.run(debug=True)