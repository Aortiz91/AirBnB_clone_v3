#!/usr/bin/python3
""" new view for State """


from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/amenities",  methods=["GET", "POST"])
def amenities():
    """ Retrieve a list of all Amenity objects """
    if request.method == "GET":
        amenityToDict = []
        amenityList = storage.all(Amenity).values()
        for item in amenityList:
            amenityToDict.append(item.to_dict())
        return jsonify(amenityToDict)
    if request.method == "POST":
        if request.headers.get("Content-Type") != "application/json":
            return jsonify("Not a JSON"), 400
        for key in request.get_json():
            if key == "name":
                newAmenity = Amenity(**(request.get_json()))  # Kwargs
                newAmenity.save()
                return jsonify(newAmenity.to_dict()), 201
        return jsonify("Missing name"), 400


@app_views.route("/amenities/<amenity_id>", methods=["GET", "DELETE", "PUT"])
def amenity(amenity_id):
    """ Retrieves a unique City object id = city_id """
    amenityById = storage.get(Amenity, amenity_id)
    if not amenityById:
        abort(404)
    if request.method == "GET":
        return jsonify(amenityById.to_dict())
    elif request.method == "DELETE":
        storage.delete(amenityById)
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
                setattr(amenityById, key, value)
        storage.save()
        return jsonify(amenityById.to_dict()), 200
