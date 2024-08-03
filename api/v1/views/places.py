#!/usr/bin/python3
"""states routers"""
from models import storage
from models.place import Place
from flask import jsonify, request, abort
from api.v1.views import app_views
