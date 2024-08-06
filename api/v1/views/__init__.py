#!/usr/bin/python3
"""
Init file for views module

This module initializes the Blueprint for the API views and imports
the view functions from various modules to register them with the
blueprint. The blueprint is then registered with the Flask application
in the main app file.
"""

from flask import Blueprint

# Initialize the Blueprint for API views
# The blueprint is used to organize the views and routes under a common URL prefix
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import view functions from the modules to register them with the blueprint
# This allows the routes defined in these modules to be accessible through the blueprint

# Import routes from the index module
from api.v1.views.index import *

# Import specific routes from the states module
from api.v1.views.states import get_states, states_id

# Import all routes from the cities module
from api.v1.views.cities import *

# Import specific routes from the amenities module
from api.v1.views.amenities import get_amenities, amenity_by_id

# Import all routes from the users module
from api.v1.views import users

# Import specific routes from the places module
from api.v1.views.places import get_places_by_city, get_places_by_id

# Import all routes from the places_reviews module
from api.v1.views.places_reviews import *

# Import all routes from the places_amenities module
from api.v1.views.places_amenities import *
