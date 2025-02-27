#!/usr/bin/python3
"""Amenity Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["GET"],
        strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["DELETE"],
        strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """Creates a Amenity"""
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400)

    try:
        new_amenity = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in new_amenity:
        return jsonify({"error": "Missing name"}), 400

    amenity_obj = Amenity(**new_amenity)
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """Updates a Amenity object"""
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    try:
        update_amenity = request.get_json()
    except Exception as e:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in update_amenity.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200
