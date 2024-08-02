#!/usr/bin/python3
"""model for route"""
from api.v1.views import *
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    result = {"status": "ok"}
    return jsonify(result)
