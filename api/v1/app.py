#!/usr/bin/python3
"""Entry Point"""


from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """closes storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Error Handler"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)