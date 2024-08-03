#!/usr/bin/python3
"""Endpoint (route) will be to return the status of your API"""

from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os

# Create a Flask app
app = Flask(__name__)

# Enable CORS : Cross-Origin Resource Sharing
CORS(app, resources={r"/*": {"origins": "*"}})

# Register the blueprint
app.register_blueprint(app_views, url_prefix="/api/v1")


# Teardown function
@app.teardown_appcontext
def close(exception):
    """Close the storage session"""
    storage.close()


# Custom error handlers
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
    """ Main Function """
    # Retrieve environment variables or set default values
    # Default to '0.0.0.0' if not set
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))  # Default to 5000 if not set

    # Run the Flask app
    app.run(host=host, port=port, threaded=True, debug=True)
