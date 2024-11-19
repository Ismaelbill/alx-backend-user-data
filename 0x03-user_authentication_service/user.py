#!/usr/bin/env python3
""" user module db
"""
from sqlalchemy import Column, Integer, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ table for storing data for a user """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
