#!/usr/bin/python3
"""places amenities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities")
def showAmenityPlace(place_id):
    """get all amenities in a place"""
    if place_id is None:
        abort(404)
    placeById = storage.get(Place, place_id)
    if placeById is None:
        abort(404)

    amenitiestoDict = []
    if storage_t != 'db':
        placeamenityList = storage.all(Amenity).values()
        for items in placeamenityList:
            if items.id in placeById.amenity_ids:
                amenitiestoDict.append(items)
    else:
        amenitiestoDict = placeById.amenities

    return jsonify([items.to_dict() for items in amenitiestoDict])


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def deleteAmenityPlace(place_id, amenity_id):
    """Deletes an amenity from a place"""
    if place_id is None or amenity_id is None:
        abort(404)
    placeById = storage.get(Place, place_id)
    amenityById = storage.get(Amenity, amenity_id)
    if placeById is None or amenityById is None:
        abort(404)

    if storage_t != 'db':
        if amenityById.id not in placeById.amenity_ids:
            abort(404)
        index = None
        for idx, id in enumerate(placeById.amenity_ids):
            if amenityById.id == id:
                index = idx
                break
        del placeById.amenity_ids[index]
        placeById.save()
    else:
        index = None
        for idx, item in enumerate(placeById.amenities):
            if item.id == amenityById.id:
                index = idx
                break
        if index is None:
            abort(404)
        del placeById.amenities[index]
        placeById.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def createAmenityPlace(place_id, amenity_id):
    """Creates an amenity of a place"""
    if place_id is None or amenity_id is None:
        abort(404)

    placeById = storage.get(Place, place_id)
    amenityById = storage.get(Amenity, amenity_id)

    if placeById is None or amenityById is None:
        abort(404)

    if storage_t != 'db':
        if amenity_id in placeById.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            placeById.amenity_ids.append(amenity_id)
            placeById.save()
            return jsonify(amenityById.to_dict()), 201
    else:
        if amenityById in placeById.amenities:
            return jsonify(amenityById.to_dict()), 200
        else:
            placeById.amenities.append(amenityById)
            placeById.save()
            return jsonify(amenityById.to_dict()), 201
