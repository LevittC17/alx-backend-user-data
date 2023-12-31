#!/usr/bin/env python3

"""
DB Module
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): User's email.
            hashed_password (str): User's hashed password.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database on the provided keyword arguments
        Args:
            **kwargs: Arbitrary keyword arguments for filtering the query
        Returns:
            NoResultFound: If no user is found
            InvalidRequestError: If wrong query arguments are passed
        """
        allowed_keys = {'id', 'email', 'hashed_password', 'session_id',
                        'reset_token'}
        invalid_keys = set(kwargs.keys()) - allowed_keys

        if invalid_keys:
            raise InvalidRequestError('Invalid query arguments')

        result = self._session.query(User).filter_by(**kwargs).first()

        if result is None:
            raise NoResultFound('No user found')

        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attribute based on the provided user_id and
        keyword argument
        Raises:
            ValueError: If an argument that doesn't correspond to a user
                        atribute is passed
        """
        user = self.find_user_by(id=user_id)
        allowed_keys = {'email', 'hashed_password', 'session_id',
                        'reset_token'}

        for key in kwargs.keys():
            if key not in allowed_keys:
                raise ValueError(f'Invalid argument: {key}')

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
