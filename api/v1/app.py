#!/usr/bin/python3
"""Endpoint (route) will be to return the status of your API"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(app_views)



@app.teardown_appcontext
def close_storage(exception):
    """tear down: close storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")

    app.run(host=host, port=int(port), threaded=True, debug=True)
