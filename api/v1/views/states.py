#!/usr/bin/python3
""" new view for State """


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/states",  methods=["GET", "POST"])
def states():
    """ Retrieve a list of all State objects """
    if request.method == "GET":
        stateToDict = []
        stateList = storage.all(State).values()
        for item in stateList:
            stateToDict.append(item.to_dict())
        return jsonify(stateToDict)
    if request.method == "POST":
        if request.headers.get("Content-Type") != "application/json":
            return jsonify("Not a JSON"), 400
        for key in request.get_json():
            if key == "name":
                newState = State(**(request.get_json()))  # Kwargs
                newState.save()
                return jsonify(newState.to_dict()), 201
        return jsonify("Missing name"), 400


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def state(state_id):
    """ Retrieves a State object """
    stateById = storage.get(State, state_id)
    if not stateById:
        abort(404)
    if request.method == "GET":
        return jsonify(stateById.to_dict())
    elif request.method == "DELETE":
        storage.delete(stateById)
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
                setattr(stateById, key, value)
        storage.save()
        return jsonify(stateById.to_dict()), 200
