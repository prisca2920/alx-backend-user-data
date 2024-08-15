#!/usr/bin/env python3
""" a hashed password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())


def _generate_uuid() -> str:
    """a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registering a new user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email, hashed)
            return user
        raise ValueError('User {} already exists' .format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """checks a valid login"""
        try:
            email = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        email_passwd = email.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, email_passwd)

    def create_session(self, email: str) -> str:
        """returns the session ID as a str"""
        try:
            email = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            email.session_id = _generate_uuid()
            return email.session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find user by session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroys a session"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """to update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
