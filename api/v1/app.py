#!/usr/bin/python3
"""
Flask Application

This module sets up the Flask application, registers blueprints,
handles CORS, and defines error handlers and teardown functions.
"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_appcontext(code):
    """ Close Storage
    This function is called when the app context is torn down. It ensures
    that the storage is properly closed.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ 404 Error Handler
    This function handles 404 errors by returning a JSON response
    with an error message.

    Parameters:
        error: The error that caused the handler to be called.

    Returns:
        A JSON response with a 404 status code and an error message.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    """ Main Function
    This function runs the Flask application with the specified host and port.
    """
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
