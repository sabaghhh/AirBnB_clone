#!/usr/bin/python3
"""
testing for City class
"""


from models.city import City
import unittest
from datetime import datetime
import uuid
import models
import time


class TestCity(unittest.TestCase):
    """
    testing for the class City
    """
    def test_init_with_no_kwargs(self):
        """
        tests if an instance is created with no args
        and checks attribute types
        """
        instance1 = City()
        time.sleep(0.5)
        instance2 = City()

        self.assertEqual(type(instance1), City)
        self.assertEqual(type(instance2), City)
        self.assertNotEqual(instance1.id, instance2.id)
        self.assertEqual(type(instance1.created_at), datetime)
        self.assertEqual(type(instance1.updated_at), datetime)
        self.assertEqual(type(instance1.id), str)
        self.assertIn(instance1, models.storage.all().values())
        self.assertIn(instance2, models.storage.all().values())
        self.assertLess(instance1.created_at, instance2.created_at)
        self.assertLess(instance1.updated_at, instance2.updated_at)
        self.assertEqual(type(instance1.state_id), str)
        self.assertEqual(type(instance1.name), str)

    def test_init_with_kwargs(self):
        """
        tests if an instance is created with kwargs
        and checks attributes
        """
        kwargs = {
                "id": str(uuid.uuid4()),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "state_id": "123",
                "name": "Cairo"
                }
        testformat = "%Y-%m-%dT%H:%M:%S.%f"
        instance1 = City(**kwargs)

        self.assertEqual(type(instance1), City)
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
        self.assertEqual(kwargs["state_id"], instance1.state_id)
        self.assertEqual(kwargs["name"], instance1.name)

        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_str_repr(self):
        """
        checks if the str returns the correct output
        """
        inst1 = City()
        rslt = f"[{inst1.__class__.__name__}] ({inst1.id}) {inst1.__dict__}"
        self.assertEqual(str(inst1), rslt)

    def test_save(self):
        """
        test saving the model
        """
        instance1 = City()
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
        instance1 = City(state_id="123123", name="asdad")
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
        self.assertEqual(instance_dict["state_id"], instance1.state_id)
        self.assertEqual(instance_dict["name"], instance1.name)

    def test_init_with_serialization(self):
        """
        serlialize and desialize models and init with them
        """
        instance1 = City(state_id="1231", name="asad")
        instance_dict = instance1.to_dict()
        instance2 = City(**instance_dict)

        self.assertEqual(instance1.id, instance2.id)
        self.assertEqual(instance1.created_at, instance2.created_at)
        self.assertEqual(instance1.updated_at, instance2.updated_at)
        self.assertEqual(instance1.state_id, instance2.state_id)
        self.assertEqual(instance1.name, instance2.name)


if __name__ == "__main__":
    unittest.main()
