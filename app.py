from flask import Flask, render_template, jsonify, request
import gmap

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ajax', methods=['POST'])
def ajax():
    data = request.get_json()
    print(data)
    a = data.split(',')[0].lstrip("(")
    b = data.split(',')[1].lstrip(" ").rstrip(")")
    loc_data = gmap.ret_location(float(a), float(b))

    return jsonify(result = "success", mydata= loc_data)

if __name__ == '__main__':
    app.run(debug=True)