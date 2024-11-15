#!/usr/bin/env python3
""" module for authenticating a user """
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def loginn():
    """loginn - func handles forms"""
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if (user.is_valid_password(password)):
            from api.v1.app import auth
            from os import getenv
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)

            return response
    return jsonify({"error": "wrong password"}), 401
