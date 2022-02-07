#!/usr/bin/python3
""" new view for place reviews """


from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, abort


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
    reviewById = storage.get(place_reviews.PlaceReview, review_id)
    if not reviewById:
        abort(404)
    if request.method == "GET":
        return jsonify(reviewById.to_dict())


@app_views.route("reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """deletes a PlaceReview"""
    reviewById = storage.get(place_reviews.PlaceReview, review_id)
    if not reviewById:
        abort(404)
    if request.method == "DELETE":
        storage.delete(reviewById)
        storage.save()
        return jsonify(reviewById.to_dict())


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """creates a PlaceReview linked to a place_id"""
    placeById = storage.get(Place, place_id)
    if not placeById:
        abort(404)
    if request.headers.get("Content-Type") != "application/json":
        return jsonify("Not a JSON"), 400
    if not request.get_json().get("user_id"):
        return jsonify("Missing user_id"), 400
    if not request.get_json().get("text"):
        return jsonify("Missing text"), 400
    userById = storage.get(User, user_id)
    if not userById:
        abort(404)
    newReview = PlaceReview(**(request.get_json()))
    newReview.place_id = place_id
    newReview.user_id = user_id
    newReview.save()
    return jsonify(newReview.to_dict()), 201


@app_views.route("/places/<place_id>/reviews/<review_id>", methods=["PUT"])
def update_review(place_id, review_id):
    """updates a PlaceReview"""
    placeById = storage.get(Place, place_id)
    if not placeById:
        abort(404)
    reviewById = storage.get(PlaceReview, review_id)
    if not reviewById:
        abort(404)
    if request.headers.get("Content-Type") != "application/json":
        return jsonify("Not a JSON"), 400
    userById = storage.get(User, user_id)
    if not userById:
        abort(404)
    reviewById.user_id = user_id
    reviewById.text = text
    reviewById.save()
    return jsonify(reviewById.to_dict()), 200
