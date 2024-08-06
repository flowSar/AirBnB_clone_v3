#!/usr/bin/python3
"""Places routers"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve places by city or create a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' not in data:
            return jsonify({'error': 'Missing user_id'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400

        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        new_place = Place(**data)
        new_place.city_id = city_id
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_places_by_id(place_id):
    """Retrieve, delete, or update a place by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400

        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
