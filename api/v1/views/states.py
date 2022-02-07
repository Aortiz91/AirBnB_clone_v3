#!/usr/bin/python3
""" new view for State """


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/states")
def states():
    """ Retrieve a list of all State objects """
    stateToDict = []
    stateList = storage.all(State).values()
    for item in stateList:
        stateToDict.append(item.to_dict())
    return jsonify(stateToDict)


@app_views.route("/states", methods=["POST"])
def create_state():
    """creates a State"""
    if request.headers.get("Content-Type") != "application/json":
        return jsonify("Not a JSON"), 400
    for key in request.get_json():
        if key == "name":
            newState = State(**(request.get_json()))  # Kwargs
            newState.save()
            return jsonify(newState.to_dict()), 201
    return jsonify("Missing name"), 400


@app_views.route("/states/<state_id>")
def state(state_id):
    """ Retrieves a State object """
    stateById = storage.get(State, state_id)
    if not stateById:
        abort(404)
    return jsonify(stateById.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """deletes a state with id state_id"""
    stateById = storage.get(State, state_id)
    if not stateById:
        abort(404)
    storage.delete(stateById)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def update_state(state_id):
    """updates a state with id state_id"""
    stateById = storage.get(State, state_id)
    if not stateById:
        abort(404)
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
