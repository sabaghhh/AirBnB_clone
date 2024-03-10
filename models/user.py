#!/usr/bin/python3
"""Module for the user class"""
from models.base_model import BaseModel


class User(BaseModel):
    """This class defines a user"""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
