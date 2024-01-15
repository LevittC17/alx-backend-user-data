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
