#!/usr/bin/python3
"""
the reviews model
"""


from models.base_model import BaseModel


class Review(BaseModel):
    """
    the reviews model
    """
    place_id = ""
    user_id = ""
    text = ""
