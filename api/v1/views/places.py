#!/usr/bin/python3
""" new view for Place """


from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/cities/<city_id>/places")
def places(city_id):
    """ Retrieve a list of all Place objects linked to a City id = city_id """
    cityById = storage.get(City, city_id)
    if not cityById:
        abort(404)
    placeToDict = []
    placeList = storage.all(Place).values()
    for item in placeList:
        if item.city_id == city_id:
            placeToDict.append(item.to_dict())
    return jsonify(placeToDict)


@app_views.route("/cities/<city_id>/places",  methods=["POST"])
def create_place(city_id):
    """creates a Place linked to a city_id"""
    cityById = storage.get(City, city_id)
    if not cityById:
        abort(404)
    if request.headers.get("Content-Type") != "application/json":
        return jsonify("Not a JSON"), 400
    if not request.get_json().get("name"):
        return jsonify("Missing name"), 400
    if not request.get_json().get("user_id"):
        return jsonify("Missing user_id"), 400
    userById = storage.get(User, request.get_json().get("user_id"))
    if not userById:
        abort(404)
    newPlace = Place(**(request.get_json()))  # Kwargs
    newPlace.city_id = city_id
    newPlace.user_id = request.get_json().get("user_id") 
    newPlace.save()
    return jsonify(newPlace.to_dict()), 201


@app_views.route("/places/<place_id>")
def place(place_id):
    """ Retrieves a unique Place object id = place_id """
    placeById = storage.get(Place, place_id)
    if not placeById:
        abort(404)
    if request.method == "GET":
        return jsonify(placeById.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """deletes a Place"""
    placeById = storage.get(Place, place_id)
    if not placeById:
        abort(404)
    storage.delete(placeById)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """updated a place"""
    placeById = storage.get(Place, place_id)
    if not placeById:
        abort(404)
    if request.headers.get("Content-Type") != "application/json":
        return jsonify("Not a JSON"), 400
    reqToJSON = request.get_json()
    for key, value in reqToJSON.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        if key == "user_id":
            continue
        else:
            setattr(placeById, key, value)
    storage.save()
    return jsonify(placeById.to_dict()), 200
