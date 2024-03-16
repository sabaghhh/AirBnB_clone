#!/usr/bin/python3
"""The module  to manage file storage for Airbnb clone"""
import json


class FileStorage:
    """Represent an abstracted storage engine."""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Return the dictionary __objects in storage"""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as jfile:
            dict_obj = {}
            dict_obj.update(FileStorage.__objects)
            for k, v in dict_obj.items():
                dict_obj[k] = v.to_dict()
            json.dump(dict_obj, jfile)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            dict_obj = {}
            with open(FileStorage.__file_path, 'r') as jfile:
                dict_obj = json.load(jfile)
                for k, v in dict_obj.items():
                        self.all()[k] = classes[v['__class__']](**v)
        except FileNotFoundError:
            pass
