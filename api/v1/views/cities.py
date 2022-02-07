#!/usr/bin/python3
""" new view for State """


from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/states/<state_id>/cities",  methods=["GET", "POST"])
def cities(state_id):
    """ Retrieve a list of all City objects linked to a State id = state_id """
    stateById = storage.get(State, state_id)
    if not stateById:
        abort(404)
    if request.method == "GET":
        cityToDict = []
        cityList = storage.all(City).values()
        for item in cityList:
            cityToDict.append(item.to_dict())
        return jsonify(cityToDict)
    if request.method == "POST":
        if request.headers.get("Content-Type") != "application/json":
            return jsonify("Not a JSON"), 400
        for key in request.get_json():
            if key == "name":
                newCity = City(**(request.get_json()))  # Kwargs
                newCity.state_id = state_id
                newCity.save()
                return jsonify(newCity.to_dict()), 201
        return jsonify("Missing name"), 400


@app_views.route("/cities/<city_id>", methods=["GET", "DELETE", "PUT"])
def city(city_id):
    """ Retrieves a unique City object id = city_id """
    cityById = storage.get(City, city_id)
    if not cityById:
        abort(404)
    if request.method == "GET":
        return jsonify(cityById.to_dict())
    elif request.method == "DELETE":
        storage.delete(cityById)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        if request.headers.get("Content-Type") != "application/json":
            return jsonify("Not a JSON"), 400
        reqToJSON = request.get_json()
        for key, value in reqToJSON.items():
            if key == "id" or key == "created_at" or key == "updated_at":
                continue
            else:
                setattr(cityById, key, value)
        storage.save()
        return jsonify(cityById.to_dict()), 200
