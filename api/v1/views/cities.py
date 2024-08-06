#!/usr/bin/python3
"""cities routers"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
def get_cities(state_id):
    """Retrieve all cities for a given state and create a new city."""
    states = storage.all(State)
    key = 'State.{}'.format(state_id)
    if key not in states:
        return abort(404)

    if request.method == 'GET':
        state = states[key]
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400

        new_city = City()
        new_city.state_id = state_id
        new_city.name = data['name']
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city_by_id(city_id):
    """Retrieve, delete or update a city by its id."""
    cities = storage.all(City)
    key = 'City.{}'.format(city_id)
    city = cities.get(key)
    if city is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400

        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
