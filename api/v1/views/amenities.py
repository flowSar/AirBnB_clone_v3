#!/usr/bin/python3
"""amenities routers"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    amenities = storage.all(Amenity)
    if request.method == 'GET':
        valid_json = []
        for amenity in amenities.values():
            valid_json.append(amenity.to_dict())
        return jsonify(valid_json)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is not None:
            if 'name' in data:
                amenity = Amenity()
                amenity.name = data.get('name')
                amenity.save()
                return jsonify(amenity.to_dict()), 201
            else:
                return jsonify({'error': 'Missing name'}), 400
        else:
            return {'error': 'Not a JSON'}, 400
    return abort(404)


@app_views.route('/amenities/<string:id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_by_id(id):
    amenities = storage.all(Amenity)
    key = f'Amenity.{id}'
    if request.method == 'GET':
        for amenity in amenities.values():
            if amenity.id == id:
                return jsonify(amenity.to_dict())

        return abort(404)
    elif request.method == 'DELETE':
        for amenity in amenities.values():
            if amenity.id == id:
                storage.delete(amenity)
                storage.save()
                return jsonify({}), 200
        return abort(404)
    elif request.method == 'PUT':
        if key in amenities:
            data = request.get_json(silent=True)
            if data is not None:
                obj = amenities.get(key)
                for k, v in data.items():
                    setattr(obj, k, v)
                obj.save()
                return jsonify(obj.to_dict()), 200
            else:
                return {'error': 'Not a JSON'}, 400
        return abort(404)
    return abort(404)
