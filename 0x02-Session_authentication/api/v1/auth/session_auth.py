#!/usr/bin/env python3
""" Module of Session
    Authentication
"""
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ SessionAuth that inherits from Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if (user_id is None or not isinstance(user_id, str)):
            return None
        id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if not (session_id or type(session_id) == str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        cookie_value = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_value)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if not(request or
                self.session_cookie(request)):
            return None
        session_id = self.session_cookie(request)
        if not self.user_id_for_session_id(session_id):
            return None
        del self.user_id_by_session_id[session_id]
        return True
