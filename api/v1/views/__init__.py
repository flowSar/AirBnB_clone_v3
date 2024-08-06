#!/usr/bin/python3
"""Init file for views Blueprint"""

from flask import Blueprint
print("Initializing Blueprint")
app_views = Blueprint('app_views', __name__)
print("Blueprint initialized")

# Import view functions from various modules to register them with the blueprint
print("Importing views")

from api.v1.views.index import *
print("Imported index views")

from api.v1.views.states import *
print("Imported states views")

from api.v1.views.cities import *
print("Imported cities views")

from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
