#!/usr/bin/python3
"""Init file for views module"""
from flask import Blueprint
from models import storage


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views import index
from api.v1.views.states import get_states, states_id
from api.v1.views.cities import *
from api.v1.views.amenities import get_amenities, amenity_by_id
from api.v1.views import users
from api.v1.views.places import get_places_by_city, get_places_by_id
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
