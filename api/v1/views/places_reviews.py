#!/usr/bin/python3
Reviews Blueprint
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from json import JSONDecodeError


@app_views.route(
        "/places/<place_id>/reviews",
        methods=["GET"],
        strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route(
        "/reviews/<review_id>",
        methods=["GET"],
        strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route(
        "/reviews/<review_id>",
        methods=["DELETE"],
        strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
        "/places/<place_id>/reviews",
        methods=["POST"],
        strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place:
        try:
            new_review = request.get_json()
        except JSONDecodeError as e:
            return jsonify({"error": "Invalid JSON"}), 400
        if not new_review:
            return jsonify({"error": "No JSON data provided"}), 400

        user_id = new_review.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get(User, user_id)
        if not user:
            abort(404)

        if "text" not in new_review:
            return jsonify({"error": "Missing text"}), 400

        review_obj = Review(**new_review)
        review_obj.place_id = place_id
        review_obj.save()
        return jsonify(review_obj.to_dict()), 201
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    try:
        update_review = request.get_json()
    except JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON"}), 400
    if not update_review:
        return jsonify({"error": "No JSON data provided"}), 400

    for key, value in update_review.items():
        if key not in [
                "id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
