#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """ method for saving the user to the database.
        """
        if not (email and hashed_password):
            return None
        try:
            new_user: User = User(email=email, hashed_password=hashed_password)
            session: Session = self._session
            session.add(new_user)
            session.commit()
            return new_user
        except Exception:
            session.rollback()
            return None

    def find_user_by(self, **kwargs):
        """ method for finding user by a given kwargs
        """
        if not kwargs:
            raise InvalidRequestError()
        session: Session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound()
        except Exception:
            raise InvalidRequestError()

    def update_user(self, user_id: int, **kwargs):
        """ method for updating a user infos by given kwargs
        """
        if user_id and kwargs:
            session: Session = self._session
            user = session.query(User).filter_by(id=user_id).one()
            for key in kwargs:
                if not hasattr(user, key):
                    raise ValueError()
                setattr(user, key, kwargs.get(key))

        return None