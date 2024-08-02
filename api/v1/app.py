#!/usr/bin/python3
"""flask app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)

@app.route('/')
def home():
    return "Hello, World!"

@app.teardown_appcontext
def tear_down(exception):
    storage.close()

if __name__ == "__main__":
    p_host = '0.0.0.0'
    p_port = 5000
    if os.getenv('HBNB_API_HOST'):
        p_host = os.getenv('HBNB_API_HOST')
    if os.getenv('HBNB_API_PORT'):
        p_port = os.getenv('HBNB_API_PORT')

    app.run(port=p_port, host=p_host, threaded=True, debug=True)
        
