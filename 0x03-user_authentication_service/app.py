#!/usr/bin/env python3
""" building app with flask
"""
from auth import Auth
from flask import Flask, jsonify, request


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def home():
    """ return a JSON"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """ method for signing up a user if does not exists
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        try:
            AUTH.register_user(email, password)
            return jsonify({"email": email, "message": "user created"}), 400
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
