#!/usr/bin/env python3
""" Register user & hashing password
"""
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ for hashing password with bcrypt """
    passw = password.encode()
    return bcrypt.hashpw(
        password=passw,
        salt=bcrypt.gensalt())


def _generate_uuid():
    """return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ checks for if user exists if not it creates one, else raise
            a value error
        """
        db = self._db
        try:
            db.find_user_by(email=email)
        except NoResultFound:
            created_user = db.add_user(email,
                                       _hash_password(password))
            return created_user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """ checking if user exists, if it matches return True.
            otherwise, return False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str):
        """ generate a new UUID and store it in
            the database as the user’s session_id,
            then returns the session ID.
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return None
        uid = _generate_uuid()
        db.update_user(user.id, session_id=uid)
        return user.session_id
