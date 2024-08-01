#!/usr/bin/env python3
"""Checking valid password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ adding a salt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check a valid password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
