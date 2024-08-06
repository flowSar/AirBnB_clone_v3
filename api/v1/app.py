#!/usr/bin/python3
"""Flask Application

This module sets up the Flask application, registers blueprints,
handles CORS, and defines error handlers and teardown functions.
"""
from models import storage
from api.v1.views.index import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS


# Initialize the Flask application
app = Flask(__name__)

# Configure the Flask application
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Register the blueprint for API views
app.register_blueprint(app_views)

# Enable CORS for the application
CORS(app, origins='0.0.0.0')

@app.teardown_appcontext
def close_db(error):
    """ Close Storage
    This function is called when the app context is torn down. It ensures
    that the storage is properly closed.
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error Handler
    This function handles 404 errors by returning a JSON response
    with an error message.

    Parameters:
        error: The error that caused the handler to be called.

    Returns:
        A JSON response with a 404 status code and an error message.
    """
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    """ Main Function
    This function runs the Flask application with the specified host and port.
    """
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(port), threaded=True, debug=True)
