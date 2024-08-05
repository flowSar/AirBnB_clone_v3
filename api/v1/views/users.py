#!/usr/bin/python3
"""User routers for handling RESTful API actions"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """Gets the list of all User objects or creates a new User.
    
    GET: Returns a list of all User objects in JSON format.
    POST: Creates a new User object and returns it in JSON format.
        - If the request body is not valid JSON, returns a 400 error.
        - If the 'email' key is missing, returns a 400 error.
        - If the 'password' key is missing, returns a 400 error.
    """
    if request.method == 'GET':
        users = storage.all(User)
        valid_json = [user.to_dict() for user in users.values()]
        return jsonify(valid_json)
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'email' not in data:
            return jsonify({'error': 'Missing email'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Missing password'}), 400
        
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def users_by_id(user_id):
    """Retrieves, deletes, or updates a User object by ID.
    
    GET: Returns the User object with the specified ID in JSON format.
        - If the User ID is not found, returns a 404 error.
    DELETE: Deletes the User object with the specified ID.
        - If the User ID is not found, returns a 404 error.
        - Returns an empty dictionary with status code 200.
    PUT: Updates the User object with the specified ID.
        - If the User ID is not found, returns a 404 error.
        - If the request body is not valid JSON, returns a 400 error.
        - Ignores keys: id, email, created_at, and updated_at.
        - Returns the updated User object in JSON format.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'Not a JSON'}), 400
        
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
