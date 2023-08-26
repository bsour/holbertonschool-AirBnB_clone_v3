#!/usr/bin/python3
"""Place Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
    "/cities/<city_id>/places",
    methods=["GET"],
    strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route(
    "/places/<place_id>",
    methods=["GET"],
    strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    "/places/<place_id>",
    methods=["DELETE"],
    strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route(
    "/cities/<city_id>/places",
    methods=["POST"],
    strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
