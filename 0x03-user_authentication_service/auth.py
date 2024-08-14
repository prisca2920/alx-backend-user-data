#!/usr/bin/env python3
""" a hashed password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    passwd = password.encode('utf-8')
    return bcrypt.hashpw(passwd, bcrypt.gensalt())
