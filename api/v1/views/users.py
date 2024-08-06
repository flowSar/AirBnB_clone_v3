#!/usr/bin/python3
"""User objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def user(user_id=None):
    """Retrieve list of users or a specific user"""
    if user_id is None:
        user_list = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(user_list)
    else:
        result = storage.get(User, user_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def user_delete(user_id):
    """Delete a user"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """Create a new user"""
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if "email" not in data:
        return jsonify({'error': 'Missing email'}), 400
    if "password" not in data:
        return jsonify({'error': 'Missing password'}), 400
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Update a user"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
