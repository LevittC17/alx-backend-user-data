#!/usr/bin/env python3

"""
Class inheritance
"""

from api.v1.auth.auth import Auth


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
