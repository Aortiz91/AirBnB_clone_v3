#!/usr/bin/python3
""" new view for place reviews """


from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def place_reviews(place_id):
    """ Retrieves a list of all PlaceReview """
    placeById = storage.get(Place, place_id)
    if not placeById:
        abort(404)
    placeReviewToDict = []
    placeReviewList = storage.all(PlaceReview).values()
    for item in placeReviewList:
        placeReviewToDict.append(item.to_dict())
    return jsonify(placeReviewToDict)


@app_views.route("reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """ Retrieves a unique PlaceReview object id = review_id """
    reviewById = storage.get(Review, review_id)
    if not reviewById:
        abort(404)
    if request.method == "GET":
        return jsonify(reviewById.to_dict())


@app_views.route("reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """deletes a PlaceReview"""
    reviewById = storage.get(Review, review_id)
    if not reviewById:
        abort(404)
    if request.method == "DELETE":
        storage.delete(reviewById)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """creates a PlaceReview linked to a place_id"""
    placeById = storage.get(Place, place_id)
    if not placeById:
        abort(404)
    if request.method == "POST":
        if not request.get_json():
            abort(400, "Not a JSON")
        if "user_id" not in request.get_json():
            abort(400, "Missing user_id")

        data = request.get_json()
        user = storage.get(User, data["user_id"])

        if not user:
            abort(404)

        if "text" not in data:
            abort(400, "Missing text")

        data["place_id"] = place_id
        review = Review(**data)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/places/<place_id>/reviews/<review_id>", methods=["PUT"])
def update_review(place_id, review_id):
    """updates a PlaceReview"""
    placeById = storage.get(Place, place_id)
    if not placeById:
        abort(404)
    reviewById = storage.get(Review, review_id)
    if not reviewById:
        abort(404)
    if request.method == "PUT":
        if not request.get_json():
            abort(400, "Not a JSON")

        ignore = ["id", "user_id", "created_at", "updated_at", "place_id"]

        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(reviewById, key, value)
        storage.save()
        return make_response(jsonify(reviewById.to_dict()), 200)
