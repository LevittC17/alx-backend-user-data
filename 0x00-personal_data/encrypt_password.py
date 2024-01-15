#!/usr/bin/env python3

"""
User passwords should NEVER be stored in
plain text in a database
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password for storing:
    Args:
        password (str): The password to hash
    Returns:
        bytes: The hashed pasword
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password
    Args:
        hashed_password (bytes): The hashed password
        password (str): The password to validate
    Returns:
        bool: True if the password is valid, False otherwise
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
