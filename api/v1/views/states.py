#!/usr/bin/python3
"""
State Blueprint route for handling State objects and operations
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from werkzeug.exceptions import BadRequest


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route(
        "/states/<state_id>",
        methods=["DELETE"],
        strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_states():
    """Creates a State"""
    try:
        new_state = request.get_json()
    except BadRequest as e:
        return jsonify({"error": "Not a JSON"}), 400

    if "name" not in new_state:
        return jsonify({"error": "Missing name"}), 400

    state_obj = State(**new_state)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        update_state = request.get_json()
    except BadRequest as e:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in update_state.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
