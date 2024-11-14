#!/usr/bin/env python3
""" Module of Session
    Authentication
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """ SessionAuth that inherits from Auth """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if not (user_id and type(user_id) == str):
            return None
        id = uuid4()
        self.user_id_by_session_id[id] = user_id
        return id
