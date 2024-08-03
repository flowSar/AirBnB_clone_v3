#!/usr/bin/python3
""" Routes for the API """
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "ok"}), 200


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Retrieves the number of each object type """
    counts_obj = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(counts_obj)
