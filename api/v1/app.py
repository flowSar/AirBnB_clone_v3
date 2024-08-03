#!/usr/bin/python3
"""Endpoint (route) will be to return the status of your API"""

import os  # Standard library import
from flask import Flask, jsonify  # Third-party imports
from flask_cors import CORS
from api.v1.views import app_views  # Local imports
from models import storage


# Create a Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_storage(exception):
    """Close the storage session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def bad_request(e):
    """Handle 400 errors"""
    message = e.description if hasattr(e, 'description') else "Bad request"
    return jsonify({"error": message}), 400


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")

    app.run(host=host, port=int(port), threaded=True, debug=True)
