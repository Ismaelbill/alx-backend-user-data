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


def _generate_uuid() -> str:
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

    def get_user_from_session_id(self, session_id: str):
        """Find user by session ID
        """
        if session_id is None:
            return None
        db = self._db
        try:
            user = db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ The method takes a single user_id integer
            rgument and returns None
        """
        db = self._db
        db.update_user(user_id=user_id, session_id=None)
        return

    def get_reset_password_token(self, email: str):
        """ if user exists it generates uuid and
            update user's 'reset_token', otherwise
            raising valueerror
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        db.update_user(user.id, reset_token=_generate_uuid())
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ method for updating password by token
        """
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        self._db.update_user(user.id,
                             hash_password=_hash_password(password),
                             reset_token=None)
