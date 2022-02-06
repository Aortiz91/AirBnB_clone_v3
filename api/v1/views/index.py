#!/usr/bin/python3
"""index"""


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ Return status OK as JSON """
    return jsonify(status="OK")
