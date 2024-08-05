#!/usr/bin/python3
""" Index module for handling API status and stats """
from api.v1.views import app_views
from flask import jsonify
from models import storage



@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ Returns the number of each object by type """
    counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(counts)
