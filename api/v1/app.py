#!/usr/bin/python3
"""Main application file"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown():
    """Close session"""
    storage.close()


if __name__ == "__main__":
    app_host = getenv("HBNB_API_HOST")
    app_port = getenv("HBNB_API_PORT")
    if app_host is None:
        app_host = "0.0.0.0"
    if app_port is None:
        app_port = 5000
    app.run(host=app_host, port=app_port)
