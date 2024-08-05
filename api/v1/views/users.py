#!/usr/bin/python3
"""user routers"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """get all users and and new user with POST request"""
    if request.method == 'GET':
        users = storage.all(User)
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
            return jsonify({'error': 'Not a JSON'}), 400


@app_views.route('/users/<string:user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """get users by id"""
    user = storage.get(User, user_id)

    if not user:
        return abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is not None:
            for k, v in data.items():
                setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({'error': 'Not a JSON'}), 400
