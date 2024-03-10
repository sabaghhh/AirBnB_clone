#!/usr/bin/python3
"""
Test Module for Amenity
"""


import uuid
from models.state import State
import unittest
from datetime import datetime
import time
import models


class TestState(unittest.TestCase):
    """
    Test cases for the amenity class
    """
    def test_init_state_with_no_kwargs(self):
        """
        tests to see if everything is working when
        a new amenity is initialized
        """
        amen1 = State()
        time.sleep(0.1)
        amen2 = State()

        self.assertEqual(type(amen1), State)
        self.assertEqual(type(amen2), State)
        self.assertNotEqual(amen1.id, amen2.id)
        self.assertEqual(type(amen1.created_at), datetime)
        self.assertEqual(type(amen1.updated_at), datetime)
        self.assertEqual(type(amen1.id), str)
        self.assertIn(amen1, models.storage.all().values())
        self.assertIn(amen2, models.storage.all().values())
        self.assertLess(amen1.created_at, amen2.created_at)
        self.assertLess(amen1.updated_at, amen2.updated_at)
        self.assertEqual(type(amen1.name), str)
        self.assertEqual(amen1.name, "")
        self.assertEqual(amen2.name, "")

    def test_init_state_from_kwargs(self):
        """
        initialize an instance from kwargs
        """
        kwargs = {
                "id": str(uuid.uuid4()),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "name": "Ahmed"
                }

        testformat = "%Y-%m-%dT%H:%M:%S.%f"
        amen1 = State(**kwargs)

        self.assertEqual(type(amen1), State)
        self.assertEqual(type(amen1.created_at), datetime)
        self.assertEqual(type(amen1.updated_at), datetime)
        self.assertEqual(type(amen1.id), str)
        self.assertEqual(amen1.id, kwargs["id"])
        self.assertEqual(
                amen1.created_at,
                datetime.strptime(kwargs["created_at"], testformat)
                )
        self.assertEqual(
                amen1.updated_at,
                datetime.strptime(kwargs["updated_at"], testformat)
                )
        self.assertEqual(amen1.name, kwargs["name"])
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_str_repr(self):
        """
        checks if the str returns the correct output
        """
        amen1 = State()
        rslt = f"[{amen1.__class__.__name__}] ({amen1.id}) {amen1.__dict__}"
        self.assertEqual(str(amen1), rslt)

    def test_save(self):
        """
        test saving the model
        """
        amen1 = State()
        updated_at = amen1.updated_at
        time.sleep(0.1)
        amen1.save()
        updated_at1 = amen1.updated_at
        time.sleep(0.1)
        amen1.save()
        self.assertLess(updated_at, updated_at1)
        self.assertLess(updated_at1, amen1.updated_at)

    def test_to_dict(self):
        """
        tests turning the model into dict
        """
        amen1 = State(name="test")
        amen_dict = amen1.to_dict()

        self.assertEqual(amen_dict["id"], amen1.id)
        self.assertEqual(
                amen_dict["created_at"],
                amen1.created_at.isoformat())
        self.assertEqual(
                amen_dict["updated_at"],
                amen1.updated_at.isoformat())
        self.assertIn("__class__", amen_dict.keys())
        self.assertEqual(
                amen_dict["__class__"], amen1.__class__.__name__)
        self.assertEqual(amen_dict["name"], amen1.name)

    def test_init_with_serialization(self):
        """
        serlialize and desialize models and init with them
        """
        amen1 = State(name="test")
        instance_dict = amen1.to_dict()
        amen2 = State(**instance_dict)

        self.assertEqual(amen1.id, amen2.id)
        self.assertEqual(amen1.created_at, amen2.created_at)
        self.assertEqual(amen1.updated_at, amen2.updated_at)
        self.assertEqual(amen1.name, amen2.name)


if __name__ == "__main__":
    unittest.main()
