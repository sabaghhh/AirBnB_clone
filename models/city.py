#!/usr/bin/python3
""" Module for the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """ The city class, with state ID and name """
    state_id = ""
    name = ""
