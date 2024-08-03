#!/usr/bin/python3

from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/states/<string:id>/cities', methods=['GET'])
def cities(id):
    states = storage.all(State)
    all_cities = storage.all(City)
    key = f'State.{id}'
    if key in states:
        cities = []
        for city in all_cities.values():
            if city.state_id == id:
                cities.append(city.to_dict())
        return jsonify(cities)
    else:
        return abort(404)
