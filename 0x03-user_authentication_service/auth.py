#!/usr/bin/env python3

"""
Hash Password
"""


import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt.hashpw with a salt
    Args:
        password (str): The password to hash
    Returns:
        bytes: The salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth():
    """
    Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
        Args:
            email (str): The email of the new user
            password (str): The password of the new user
        Returns:
            User: The newly created User object
        """
        # Check if the user with the given email already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass  # Continue with user registration

        # Hash the password
        hashed_password = _hash_password(password)

        # Create and add the new user to the database
        new_user = self._db.add_user(email, hashed_password)

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials
        Args:
            email (str): The email of the user
            password (str): The password to check
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            provided_password = password.encode('utf-8')
            return bcrypt.checkpw(provided_password, hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid() -> str:
        """
        Generate a new UUID
        Returns:
            str: String representation of the new UUID
        """
        return str(uuid.uuid4())
