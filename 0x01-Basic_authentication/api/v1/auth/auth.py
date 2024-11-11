#!/usr/bin/env python3
""" Module - authentication
"""
from typing import List, TypeVar


class Auth:
    """
    Auth class is the template
    for all authentication system we will implement
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth -
            returns True if the path is not in
            the list of strings excluded_paths
        """
        if (path is None or
                not excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """If request.headers does
        contain the header key Authorization returns it,
        otherwise None
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user func"""
        return None
