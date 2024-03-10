#!/usr/bin/python3
"""
first storage engine
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import os


class FileStorage:
    """
    the file storage engine
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns the dictiory of Objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        adds the new model to the objects
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """
        serialize the object to dictionary and save to file
        """
        obj_dict = {}
        for key, value in FileStorage.__objects.items():
            obj_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """
        reloads objects from file to __objects
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    cl_obj = eval(value["__class__"])(**value)
                    FileStorage.__objects[key] = cl_obj
