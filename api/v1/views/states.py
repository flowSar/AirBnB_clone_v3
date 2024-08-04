#!/usr/bin/python3
"""states routers"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """Retrieve all states and convert them to valid json with to_dict"""
    if request.method == 'GET':
        all_states = storage.all(State)
        valid_json = []
        for obj in all_states.values():
            valid_json.append(obj.to_dict())
        return jsonify(valid_json)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is not None:
            if 'name' in data:
                state = State()
                state.name = data.get('name')
                state.save()
                return jsonify(state.to_dict()), 201
            else:
                return jsonify({'error': 'Missing name'}), 400
        else:
            return {'error': 'Not a JSON'}, 400


@app_views.route('/states/<string:id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_id(id):
    """Retrieve and delete and update state based on id"""
    all_states = storage.all(State)
    key = f'State.{id}'
    if request.method == 'GET':
        if key in all_states:
            return jsonify(all_states.get(key).to_dict())
        return abort(404)
    elif request.method == 'DELETE':
        if key in all_states:
            storage.delete(all_states.get(key))
            storage.save()
            return jsonify({}), 200
        return abort(404)
    elif request.method == 'PUT':
        if key in all_states:
            data = request.get_json(silent=True)
            if data is not None:
                obj = all_states.get(key)
                for k, v in data.items():
                    setattr(obj, k, v)
                obj.save()
                return jsonify(obj.to_dict()), 200
            else:
                return {'error': 'Not a JSON'}, 400
        return abort(404)
    return abort(404)
