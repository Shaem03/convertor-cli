from decimal import Decimal

from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS
from forex_python.converter import CurrencyRates

from Convertor import Convertor

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
c = CurrencyRates()


@app.route("/", methods=["POST"])
def hello():
    return "Hi"


@app.route("/get_convert_rate", methods=["POST"])
@cache.cached(timeout=50, key_prefix='convert_rate')
def get_convert_rate():
    data = request.get_json()
    convert_to = data["convertTo"]
    try:
        convertor = Convertor()
        convert_rate = convertor.get_rates(convert_to)
        cache.set("convert_rate", convert_rate)
    except:
        convert_rate = cache.get("convert_rate")
    return convert_rate


@app.route("/convert", methods=["POST"])
def convert():
    # check the valid input
    convert_from = request.json.get("convertFrom")
    convert_to = request.json.get("convertTo")
    convert_amount = request.json.get("convertAmount")
    converted_amount = c.convert(convert_from, convert_to, Decimal(convert_amount))
    output = {'value': converted_amount,
              'currency': convert_to}
    return output, 201


if __name__ == '__main__':
    app.run(debug=True, port=5001)
