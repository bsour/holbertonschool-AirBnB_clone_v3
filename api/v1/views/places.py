#!/usr/bin/python3
"""
route for handling Place objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    retrieves all Place objects by city
    :return: json of all Places
    """
    place_list = []
    city_obj = storage.get("City", str(city_id))
    
    if not city_obj:
        abort(404, "City not found")
    
    for obj in city_obj.places:
        place_list.append(obj.to_json())

    return jsonify(place_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if "name" not in place_json:
        abort(400, 'Missing name')
    
    user_id = place_json["user_id"]
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_json["city_id"] = city_id

    new_place = Place(**place_json)
    new_place.save()
    resp = jsonify(new_place.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    fetched_obj = storage.get(Place, place_id)

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')

    fetched_obj = storage.get(Place, place_id)

    if fetched_obj is None:
        abort(404)

    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, val in place_json.items():
        if key not in ignore_keys:
            setattr(fetched_obj, key, val)

    fetched_obj.save()

    return jsonify(fetched_obj.to_dict())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    fetched_obj = storage.get(Place, place_id)

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})
