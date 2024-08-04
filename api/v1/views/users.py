#!/usr/bin/python3
"""user routers"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """Retrieve all user and convert them to valid json with to_dict"""
    users = storage.all(User)
    if request.method == 'GET':
        valid_json = []
        for user in users.values():
            valid_json.append(user.to_dict())
        return jsonify(valid_json)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is not None:
            if 'email' in data:
                if 'password' in data:
                    user = User()
                    user.email = data.get('email')
                    user.password = data.get('password')
                    user.save()
                    return jsonify(user.to_dict()), 201
                else:
                    return jsonify({'error': 'Missing password'}), 400
            else:
                return jsonify({'error': 'Missing email'}), 400
        else:
            return {'error': 'Not a JSON'}, 400
    return abort(404)


@app_views.route('/users/<string:user_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def users_by_id(user_id):
    """Retrieve and delete and update user based on id"""
    users = storage.all(User)
    key = f'User.{user_id}'
    if request.method == 'GET':
        for user in users.values():
            if user.id == user_id:
                return jsonify(user.to_dict())

        return abort(404)
    elif request.method == 'DELETE':
        for user in users.values():
            if user.id == user_id:
                storage.delete(user)
                storage.save()
                return jsonify({}), 200
        return abort(404)
    elif request.method == 'PUT':
        if key in users:
            data = request.get_json(silent=True)
            if data is not None:
                obj = users.get(key)
                for k, v in data.items():
                    setattr(obj, k, v)
                obj.save()
                return jsonify(obj.to_dict()), 200
            else:
                return {'error': 'Not a JSON'}, 400
        return abort(404)
    return abort(404)
