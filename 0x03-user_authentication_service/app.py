#!/usr/bin/env python3
"""creating a basic flask app"""
from flask import Flask, jsonify, request, abort
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """implement a login function"""
    email = request.form.get('email')
    password = request.form.get('password')

    user = AUTH.valid_login(email, password)

    if user:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
