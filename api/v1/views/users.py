#!/usr/bin/python3
""" new view for User """


from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/users")
def users():
    """ Retrieve a list of all User objects """
    userToDict = []
    userList = storage.all(User).values()
    for item in userList:
        userToDict.append(item.to_dict())
    return jsonify(userToDict)


@app_views.route("/users",  methods=["POST"])
def create_user():
    """creates a new object user"""
    if request.headers.get("Content-Type") != "application/json":
        return jsonify("Not a JSON"), 400
    if not request.get_json().get("email"):
        return jsonify("Missing email"), 400
    if not request.get_json().get("password"):
        return jsonify("Missing password"), 400
    newUser = User(**(request.get_json()))  # Kwargs
    newUser.save()
    return jsonify(newUser.to_dict()), 201


@app_views.route("/users/<user_id>")
def user(user_id):
    """ Retrieves a unique User object id = user_id """
    userById = storage.get(User, user_id)
    if not userById:
        abort(404)
    return jsonify(userById.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def del_user(user_id):
    """ Deletes a user"""
    userById = storage.get(User, user_id)
    if not userById:
        abort(404)
    storage.delete(userById)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """update information about a user"""
    userById = storage.get(User, user_id)
    if not userById:
        abort(404)
    if request.headers.get("Content-Type") != "application/json":
        return jsonify("Not a JSON"), 400
    reqToJSON = request.get_json()
    for key, value in reqToJSON.items():
        if key == "id" or key == "email":
            continue
        if key == "created_at" or key == "updated_at":
            continue
        else:
            setattr(userById, key, value)
    storage.save()
    return jsonify(userById.to_dict()), 200
