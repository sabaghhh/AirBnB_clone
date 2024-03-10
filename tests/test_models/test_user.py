#!/usr/bin/python3
"""
testing for User class
"""


from models.user import User
import unittest
import models
from datetime import datetime
import time
import uuid


class TestUser(unittest.TestCase):
    """
    testing for the class User
    """
    def test_init_with_no_kwargs(self):
        """
        tests if an instance is created with no args
        and checks attribute types
        """
        instance1 = User()
        time.sleep(0.5)
        instance2 = User()

        self.assertEqual(type(instance1), User)
        self.assertEqual(type(instance2), User)
        self.assertNotEqual(instance1.id, instance2.id)
        self.assertEqual(type(instance1.created_at), datetime)
        self.assertEqual(type(instance1.updated_at), datetime)
        self.assertEqual(type(instance1.id), str)
        self.assertIn(instance1, models.storage.all().values())
        self.assertIn(instance2, models.storage.all().values())
        self.assertLess(instance1.created_at, instance2.created_at)
        self.assertLess(instance1.updated_at, instance2.updated_at)
        self.assertEqual(type(instance1.email), str)
        self.assertEqual(type(instance1.password), str)
        self.assertEqual(type(instance1.first_name), str)
        self.assertEqual(type(instance1.last_name), str)

    def test_init_with_kwargs(self):
        """
        tests if an instance is created with kwargs
        and checks attributes
        """
        kwargs = {
                "id": str(uuid.uuid4()),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "email": "ahmed@123",
                "password": "123",
                "first_name": "Ahmed",
                "last_name": "Abd El Hameed"
                }
        testformat = "%Y-%m-%dT%H:%M:%S.%f"
        instance1 = User(**kwargs)

        self.assertEqual(type(instance1), User)
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
        self.assertEqual(instance1.email, kwargs["email"])
        self.assertEqual(instance1.password, kwargs["password"])
        self.assertEqual(instance1.first_name, kwargs["first_name"])
        self.assertEqual(instance1.last_name, kwargs["last_name"])

        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_str_repr(self):
        """
        checks if the str returns the correct output
        """
        inst1 = User()
        rslt = f"[{inst1.__class__.__name__}] ({inst1.id}) {inst1.__dict__}"
        self.assertEqual(str(inst1), rslt)

    def test_save(self):
        """
        test saving the model
        """
        instance1 = User()
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
        instance1 = User(
                email="ahmed@123",
                password="123",
                first_name="ahmed",
                last_name="AbdelElHameed"
                )
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
        self.assertEqual(instance_dict["email"], instance1.email)
        self.assertEqual(instance_dict["password"], instance1.password)
        self.assertEqual(instance_dict["first_name"], instance1.first_name)
        self.assertEqual(instance_dict["last_name"], instance1.last_name)

    def test_init_with_serialization(self):
        """
        serlialize and desialize models and init with them
        """
        instance1 = User(
                email="ahmed@123",
                password="123",
                first_name="ahmed",
                last_name="AbdelElHameed"
                )
        instance_dict = instance1.to_dict()
        instance2 = User(**instance_dict)

        self.assertEqual(instance1.id, instance2.id)
        self.assertEqual(instance1.created_at, instance2.created_at)
        self.assertEqual(instance1.updated_at, instance2.updated_at)
        self.assertEqual(instance1.email, instance2.email)
        self.assertEqual(instance1.password, instance2.password)
        self.assertEqual(instance1.first_name, instance2.first_name)
        self.assertEqual(instance1.last_name, instance2.last_name)


if __name__ == "__main__":
    unittest.main()
