#!/usr/bin/python3
"""User Blueprint"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from json import JSONDecodeError


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """Creates a User"""
    try:
        new_user = request.get_json()
    except JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON"}), 400

    if not new_user:
        return jsonify({"error": "No JSON data provided"}), 400

    if "email" not in new_user:
        return jsonify({"error": "Missing email"}), 400

    if "password" not in new_user:
        return jsonify({"error": "Missing password"}), 400

    user_obj = User(**new_user)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        update_user = request.get_json()
    except JSONDecodeError as e:
        return jsonify({"error": "Invalid JSON"}), 400

    if not update_user:
        return jsonify({"error": "No JSON data provided"}), 400

    for key, value in update_user.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
