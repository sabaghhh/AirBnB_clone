#!/usr/bin/python3
"""
the User Class
"""


from models.base_model import BaseModel


class User(BaseModel):
    """
    the User Class
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
