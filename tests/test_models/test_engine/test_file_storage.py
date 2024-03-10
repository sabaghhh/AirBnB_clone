#!/usr/bin/python3
"""
testing the file storage module
"""


from models.engine.file_storage import FileStorage
import unittest
from models.base_model import BaseModel
from models.user import User

class TestStorage(unittest.TestCase):
    """
    this is the test class of the storage
    """
    def test_init(self):
        """
        testing the initialization of the filestorage
        """
        storage = FileStorage()

        self.assertEqual(type(storage), FileStorage)
        self.assertEqual(type(storage._FileStorage__file_path), str)
        self.assertEqual(type(storage._FileStorage__objects), dict)

    def test_all(self):
        """
        tests the all function of storage
        """
        storage = FileStorage()
        store_dict = storage.all()

        self.assertEqual(type(store_dict), dict)

    def test_new(self):
        """
        tests the new function of storage test
        """
        storage = FileStorage()
        basemodel = BaseModel()
        rslt = f"{basemodel.__class__.__name__}.{basemodel.id}"
        store_dict = storage.all()

        storage.new(basemodel)
        
        self.assertIn(rslt, store_dict.keys())

    def test_save(self):
        """
        tests the save function
        """
        storage = FileStorage()
        basemodel = BaseModel()
        store_dict = storage.all()
        rslt = f"{basemodel.__class__.__name__}.{basemodel.id}"

        storage.new(basemodel)
        storage.save()

        with open("file.json", "r", encoding="utf-8") as f:
            f_read = f.read()
            self.assertIn(rslt, f_read)

        with self.assertRaises(TypeError):
            storage.save(None)

    def test_reload(self):
        """
        test the reload function
        """

        storage = FileStorage()
        basemodel = BaseModel()
        store_dict = storage.all()
        rslt = f"{basemodel.__class__.__name__}.{basemodel.id}"

        storage.new(basemodel)
        storage.save()
        storage.reload()

        obj_dict = storage._FileStorage__objects

        self.assertIn(rslt, obj_dict)



if __name__ == "__main__":
    unittest.main() 
