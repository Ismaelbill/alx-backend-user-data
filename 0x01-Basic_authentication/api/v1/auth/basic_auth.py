#!/usr/bin/env python3
""" Module - Basic Authentication """
from .auth import Auth
import base64
from typing import Tuple, TypeVar
import fnmatch
from models.user import User


class BasicAuth(Auth):
    """  BasicAuth - inherits from Auth """
    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str) -> str:
        """  returns the Base64 part of the Authorization
             header for a Basic Authentication"""
        if (authorization_header is None or
                type(authorization_header) is not str or
                authorization_header.split()[0] != 'Basic'):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
                                self, base64_authorization_header: str) -> str:
        """returns the decoded value of a
        Base64 string base64_authorization_header"""
        if (base64_authorization_header is None or
                type(base64_authorization_header) != str):
            return None
        try:

            decoded = base64.b64decode(base64_authorization_header,
                                       validate=True)
            return decoded.decode()
        except Exception:
            return None

    def extract_user_credentials(
                                self,
                                decoded_base64_authorization_header: str
                                ) -> Tuple[str, str]:
        """returns the user email and password
        from the Base64 decoded value."""
        if (decoded_base64_authorization_header is None or
                type(decoded_base64_authorization_header) is not str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        splitted_str = decoded_base64_authorization_header.split(':')
        return (splitted_str[0], splitted_str[1])

    def user_object_from_credentials(
                                    self,
                                    user_email: str,
                                    user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password."""
        if not (user_email or user_pwd or
                type(user_email) == str or
                type(user_pwd) == str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None
