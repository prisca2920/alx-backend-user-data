#!/usr/bin/env python3
"""class SessionAuth"""
import base64
from uuid import uuid4
from typing import TypeVar
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Implement Session Authorization."""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """a Session ID for a user with id user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid4()
        self.user_id_by_session_id[str(session_id)] = user_id
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a user ID based on a session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """a User instance based on a cookie valuE"""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes a user session"""
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
