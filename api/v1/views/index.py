#!/usr/bin/python3
"""index"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """ Return status OK as JSON """
    return jsonify(status="OK")


@app_views.route("/stats")
def stats():
    """ Return total of each object"""
    stats = {}
    stats["amenities"] = storage.count(Amenity)
    stats["cities"] = storage.count(City)
    stats["places"] = storage.count(Place)
    stats["reviews"] = storage.count(Review)
    stats["states"] = storage.count(State)
    stats["users"] = storage.count(User)
    return jsonify(stats)
