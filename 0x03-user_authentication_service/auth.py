#!/usr/bin/env python3
""" a hashed password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


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
