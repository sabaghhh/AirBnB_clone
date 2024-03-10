#!/usr/bin/python3
"""
test modules for the base class
"""


import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid
import models
import time


class TestBaseModel(unittest.TestCase):
    """
    the main test class for baes model
    """
    def test_init_with_no_kwargs(self):
        """
        tests if an instance is created with no args
        and checks attribute types
        """
        instance1 = BaseModel()
        time.sleep(0.5)
        instance2 = BaseModel()

        self.assertEqual(type(instance1), BaseModel)
        self.assertEqual(type(instance2), BaseModel)
        self.assertNotEqual(instance1.id, instance2.id)
        self.assertEqual(type(instance1.created_at), datetime)
        self.assertEqual(type(instance1.updated_at), datetime)
        self.assertEqual(type(instance1.id), str)
        self.assertIn(instance1, models.storage.all().values())
        self.assertIn(instance2, models.storage.all().values())
        self.assertLess(instance1.created_at, instance2.created_at)
        self.assertLess(instance1.updated_at, instance2.updated_at)

    def test_init_with_kwargs(self):
        """
        tests if an instance is created with kwargs
        and checks attributes
        """
        kwargs = {
                "id": str(uuid.uuid4()),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
                }
        testformat = "%Y-%m-%dT%H:%M:%S.%f"
        instance1 = BaseModel(**kwargs)

        self.assertEqual(type(instance1), BaseModel)
        self.assertEqual(type(instance1.created_at), datetime)
        self.assertEqual(type(instance1.updated_at), datetime)
        self.assertEqual(type(instance1.id), str)
        self.assertEqual(instance1.id, kwargs["id"])
        self.assertEqual(
                instance1.created_at,
                datetime.strptime(kwargs["created_at"], testformat)
                )
        self.assertEqual(
                instance1.updated_at,
                datetime.strptime(kwargs["updated_at"], testformat)
                )
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_str_repr(self):
        """
        checks if the str returns the correct output
        """
        inst1 = BaseModel()
        rslt = f"[{inst1.__class__.__name__}] ({inst1.id}) {inst1.__dict__}"
        self.assertEqual(str(inst1), rslt)

    def test_save(self):
        """
        test saving the model
        """
        instance1 = BaseModel()
        updated_at = instance1.updated_at
        time.sleep(0.1)
        instance1.save()
        updated_at1 = instance1.updated_at
        time.sleep(0.1)
        instance1.save()
        self.assertLess(updated_at, updated_at1)
        self.assertLess(updated_at1, instance1.updated_at)

    def test_to_dict(self):
        """
        tests turning the model into dict
        """
        instance1 = BaseModel()
        instance_dict = instance1.to_dict()

        self.assertEqual(instance_dict["id"], instance1.id)
        self.assertEqual(
                instance_dict["created_at"],
                instance1.created_at.isoformat())
        self.assertEqual(
                instance_dict["updated_at"],
                instance1.updated_at.isoformat())
        self.assertIn("__class__", instance_dict.keys())
        self.assertEqual(
                instance_dict["__class__"], instance1.__class__.__name__)

    def test_init_with_serialization(self):
        """
        serlialize and desialize models and init with them
        """
        instance1 = BaseModel()
        instance_dict = instance1.to_dict()
        instance2 = BaseModel(**instance_dict)

        self.assertEqual(instance1.id, instance2.id)
        self.assertEqual(instance1.created_at, instance2.created_at)
        self.assertEqual(instance1.updated_at, instance2.updated_at)


if __name__ == "__main__":
    unittest.main()
