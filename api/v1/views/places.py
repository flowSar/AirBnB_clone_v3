#!/usr/bin/python3
"""users routers"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """handel GET/POST request fo /cities/<string:city_id>/places route"""
    cities = storage.all(City)
    places = storage.all(Place)
    key = f'City.{city_id}'

    if key not in cities:
        return abort(404)
    if request.method == 'GET':
        found_places = []
        for place in places:
            if place.city_id == city_id:
                found_places.append(place)
        return jsonify(found_places)
    if request.method == 'POST':
        data = request.get_json(silent=True)
        if data:
            if 'user_id' in data and 'name' in data:
                users = storage.all(User)
                if data.get('user_id') in users:
                    place = Place()
                    place.name = data.get('name')
                    place.user_id = data.get('user_id')
                    storage.save()
                    return jsonify(palce.to_dict()), 201
                else:
                    return abort(404)
            else:
                if not data.get('name'):
                    return {'error': 'Missing name'}, 400
                if not data.get('user_id'):
                    return {'error': 'Missing user_id'}, 400
        else:
            return {'error': 'Not a JSON'}, 400


@app_views.route('/places/<string:place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_places_by_id(place_id):
    """handel GET DELETE PUT request fo /place/place_id route"""
    places = storage.all(Place)
    key = f'Place.{place_id}'
    to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    if key not in places:
        return abort(404)

    if request.method == 'GET':
        return jsonify(places.get(key).to_dict())
    elif request.method == 'DELETE':
        storage.delete(places.get(key))
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data:
            place = places.get(key)
            for k, v in data:
                if k not in to_ignore:
                    setattr(place, k, v)
            storage.save()
            return jsonify(place.to_dict()), 200
        else:
            return {'error': 'Not a JSON'}, 400
