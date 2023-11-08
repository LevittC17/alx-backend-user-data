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
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return False

        # Check if the path (with or without a trailing slash) is in the
        # excluded_paths
        normalized_path = path.rstrip('/')
        return normalized_path not in excluded_paths

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
