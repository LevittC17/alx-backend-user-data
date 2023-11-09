#!/usr/bin/env python3

"""
Create a class to manage the API authentication
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """
    Class template for all authentication system to implement
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Placeholder for requiring authentication
        Args:
          path (str): The requested path
          excluded_paths (List[str]): List of excluded paths
        Returns:
          - bool: False for now
        """
        if not path or not excluded_paths or not excluded_paths \
                or not path.strip('/'):
            return True

        normalized_path = path.rstrip('/') + '/'

        return not any(normalized_path.startswith(e.rstrip('/') + '/')
                       for e in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """
        Placeholder for getting the authorization header
        Args:
          request (Flask request): The flask request object
        Returns:
          - str: None for now
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder for getting the current user
        Args:
          request (Flask request): The flask request object
        Returns:
          TypeVar('User'): None for now
        """
        return None
