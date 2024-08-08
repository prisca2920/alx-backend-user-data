#!/usr/bin/env python3
""" Index views module"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """unauthorized access"""
    abort(401, description='Unauthorized')


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """forbidden description"""
    abort(403, description='Forbidden')


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ no. of each objects"""
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
