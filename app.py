from flask import Flask
import flask
import json

app = Flask(__name__)


@app.route("/trips", methods=['GET'])
def home():
    f = open('./website/JSON/trips.json')
    data = json.load(f)
    data = flask.jsonify(data)
    data.headers.add('Access-Control-Allow-Origin', '*')
    return data
