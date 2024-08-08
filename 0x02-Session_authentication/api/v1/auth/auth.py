#!/usr/bin/env python3
"""authentication module"""
from typing import List, TypeVar
from flask import request
import os


class Auth:
    """authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """whether a given path requires authentication or not"""
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*":
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from request obj"""
        if request is None:
            return None
        header = request.headers.get('Authorization')

        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a User instance from request obj"""

        return None

    def session_cookie(self, request=None):
        """Returns a cookie from a request"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
