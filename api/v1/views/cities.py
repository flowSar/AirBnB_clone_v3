#!/usr/bin/python3
"""cities routers"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:id>/cities', methods=['GET', 'POST', 'PUT'],
                 strict_slashes=False)
def get_cities(id):
    states = storage.all(State)
    all_cities = storage.all(City)
    key = f'State.{id}'
    if request.method == 'GET':
        if key in states:
            cities = []
            for city in all_cities.values():
                if city.state_id == id:
                    cities.append(city.to_dict())
            return jsonify(cities)
        else:
            return abort(404)
    elif request.method == 'POST':
        if key in states:
            obj = states.get(key)
            data = request.get_json(silent=True)
            if data is not None:
                if 'name' in data:
                    city = City()
                    city.name = data.get('name')
                    city.state_id = id
                    city.save()
                    return jsonify(city.to_dict()), 201
                else:
                    return jsonify({'error': 'Missing name'}), 400
            else:
                return {'error': 'Not a JSON'}, 400
        else:
            return abort(404)


@app_views.route('/cities/<string:id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_cities_by_id(id):
    cities = storage.all(City)
    key = f'City.{id}'
    if request.method == 'GET':
        if key in cities:
            return jsonify(cities.get(key).to_dict())
        return abort(404)
    elif request.method == 'DELETE':
        if key in cities:
            storage.delete(cities.get(key))
            storage.save()
            return jsonify({}), 200
        return abort(404)
    elif request.method == 'PUT':
        if key in cities:
            data = request.get_json(silent=True)
            if data is not None:
                obj = cities.get(key)
                for k, v in data.items():
                    setattr(obj, k, v)
                obj.save()
                return jsonify(obj.to_dict()), 200
            else:
                return {'error': 'Not a JSON'}, 400
        return abort(404)
