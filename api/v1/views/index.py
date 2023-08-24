#!/usr/bin/python3
"""blueprint index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'])
def status():
    """return status JSON"""
    return jsonify({"status": "OK"})
