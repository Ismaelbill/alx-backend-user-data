#!/usr/bin/env python3
""" Register user & hashing password
"""
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ for hashing password with bcrypt """
    passw = password.encode()
    return bcrypt.hashpw(
        password=passw,
        salt=bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ checks for if user exists if not it creates one, else raise
            a value error
        """
        if email and password:
            try:
                self._db.find_user_by(email=email)
            except NoResultFound:
                created_user = self._db.add_user(email,
                                                 _hash_password(password))
                self._db._session.commit
                return created_user
            raise ValueError(f'User {email} already exists')
