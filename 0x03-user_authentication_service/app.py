#!/usr/bin/env python3
"""creating a basic flask app"""
from flask import Flask, jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """defining the base flask"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """registering new users"""
    email = request.form.get('email')
    passwd = request.form.get('password')

    try:
        user = AUTH.register_user(email, passwd)
        return jsonify({"email": f"{email}", "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
