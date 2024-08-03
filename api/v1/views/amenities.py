#!/usr/bin/python3
"""states routers"""
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, abort
from api.v1.views import app_views
