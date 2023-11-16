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


def _generate_uuid() -> str:
    """
    Generate a new UUID
    Returns:
        str: String representation of the new UUID
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """
        Create a session for the user with the given email
        Args:
            email (str): The email of the user
        Returns:
            str: The generated session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(uuid.uuid4())
            user.session_id = session_id

            # Save the updated user with the new session_id to db
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get the user corresponding to the given session ID
        Args:
            session_id (str): The session ID to look up
        Returns:
            User: The corresponding User object if found, else None
        """
        try:
            # Try to find the user by session ID
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the user with the given user ID
        Args:
            user_id (int): The ID of the user
        Returns:
            None
        """
        try:
            # Get the user by user ID
            user = self._db.find_user_by(id=user_id)

            # Update the user's session ID to None
            self._db.update_user(user_id, session_id=None)

        except NoResultFound:
            # User not found, do nothing
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for the user
        Args:
            email (str): The email of the user
        Returns:
            str: The generated reset password token
        Raises:
            ValueError: If the user does not exist
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        # Generate a UUID for the reset password token
        reset_token = _generate_uuid()

        # Update the user's reset_token field in the db
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using the reset token
        Args:
            reset_token (str): The reset token
            password (str): The new password
        Returns:
            None
        Raises:
            ValueError: If the reset_token is not found
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
