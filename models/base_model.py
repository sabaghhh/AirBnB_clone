#!/usr/bin/python3
"""Module for the Base Class for all models in Airbnb clone"""
import uuid
from datetime import datetime


class BaseModel:
    """The base class for all models"""
    def __init__(self, *args, **kwargs):
        """The class instance initilization"""
        if kwargs:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)

        else:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)


    def __str__(self):
        """Return string reprsentation of instance"""
        cls_n = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls_n, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with the current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary with all keys/values of the instance"""
        my_dict = {}
        my_dict.update(self.__dict__)
        my_dict.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        return my_dict
