#!/usr/bin/env python3
""" building app with flask
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for


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
    email: str = request.form.get('email')
    password: str = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def log_in():
    """ user log in if exists sets a cookie,
        otherwise 401 is returned
    """
    email: str = request.form.get('email')
    password: str = request.form.get('password')
    if AUTH.valid_login(email, password):
        sid = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", sid)
        return response
    return abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """  If the user exists destroy the session
         and redirect the user to home, otherwise
         abort 403
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'))
    abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """ checks if user exists by session_id
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    if user:
        return jsonify({"email": user.email})


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """ it resets the user's token
    """
    email = request.form.get('email')
    try:
        AUTH._db.find_user_by(email=email)
    except Exception:
        abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ updates the password if token is valid,
        otherwise 403 is sent
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
