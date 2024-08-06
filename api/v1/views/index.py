#!/usr/bin/python3
""" Index module for handling API status and stats """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """
    Returns the status of the API

    This route returns a simple JSON response indicating the status of the API.

    Methods:
        GET: Returns a JSON object with the key "status" and value "OK".

    Returns:
        Response: A JSON object indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Returns the number of each object by type

    This route returns a JSON response with the counts of various objects
    managed by the storage engine. It provides a summary of the current
    statistics for each object type.

    Methods:
        GET: Returns a JSON object with the counts of each object type.

    Returns:
        Response: A JSON object containing counts of each object type.
    """
    counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(counts)


if __name__ == "__main__":
    pass
