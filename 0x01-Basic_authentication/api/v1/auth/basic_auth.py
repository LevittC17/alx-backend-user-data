#!/usr/bin/env python3

"""
Class inheritance
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """
    Initialized a class to inherit from Auth Class
    Returns:
      - Empty for now
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Auth
        """
        if authorization_header is None or not isinstance(
                authorization_header, str) or not \
                authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        Decodes the Base64 Authorization header for Basic Auth
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decode_bytes = base64.b64decode(base64_authorization_header)
            decode_string = decode_bytes.decode('utf-8')
            return decode_string
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decode_base64_authorization_header:
                                 str) -> (str, str):
        """
        Extract user email and password from the Base64 decode value
        """
        if decode_base64_authorization_header is None or not isinstance(
                decode_base64_authorization_header, str) or ":" not in \
                decode_base64_authorization_header:
            return None, None

        user_email, user_password = decode_base64_authorization_header.split(
            ":", 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """ Returns the User instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str) \
                or user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

        return users[0] if users else None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request
        """
        if request is None or not hasattr(request, 'headers'):
            return None

        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            return None

        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header)
        if base64_authorization_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(
            base64_authorization_header)
        if decoded_header is None:
            return None

        user_email, user_password = self.extract_user_credentials(
            decoded_header)
        if user_email is None or user_password is None:
            return None

        return self.user_object_from_credentials(user_email, user_password)
