#!/usr/bin/python3
"""City Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from json import JSONDecodeError


@app_views.route(
        "/states/<state_id>/cities",
        methods=["GET"],
        strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])
    abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route(
        "/states/<state_id>/cities",
        methods=["POST"],
        strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state:
        try:
            new_city = request.get_json()
        except JSONDecodeError as e:
            return jsonify({"error": "Invalid JSON"}), 400

        if not new_city:
            return jsonify({"error": "No JSON data provided"}), 400

        if "name" not in new_city:
            return jsonify({"error": "Missing name"}), 400

        city_obj = City(**new_city)
        city_obj.state_id = state_id
        city_obj.save()
        return jsonify(city_obj.to_dict()), 201
    abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "City not found"}), 404

    try:
        update_city = request.get_json()
    except JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON"}), 400

    if not update_city:
        return jsonify({"error": "No JSON data provided"}), 400

    for key, value in update_city.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict()), 200
