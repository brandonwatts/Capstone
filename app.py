#!flask/bin/python
from flask import Flask, url_for
from costar_api import costar_api_mock
import simplejson as json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index'

@app.route('/costar_api/<string:json_query>')
def costar_api(json_query):
    return costar_api_mock(json_query)

if __name__ == '__main__':
    app.run(debug=True)