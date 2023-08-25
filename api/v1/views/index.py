#!/usr/bin/python3
"""blueprint index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    """return status JSON"""
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=['GET'])
def stats():
    """return the number of instances for each class"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
