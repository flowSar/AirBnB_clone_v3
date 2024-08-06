#!/usr/bin/python3
"""
Contains the FileStorage class for serializing
and deserializing instances to/from a JSON file.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Mapping of class names to class objects for deserialization
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class FileStorage:
    """Handles serialization and deserialization
    of instances to/from a JSON file."""

    __file_path = "file.json"  # Path to the JSON file
    __objects = {}  # Dictionary to store all objects by <class name>.id

    def all(self, cls=None):
        """
        Returns a dictionary of all objects, or objects of a specified class.
        Parameters:
        cls: class (optional) - filter objects by this class

        Returns:
        Dictionary of objects matching the specified class,
        or all objects if no class is specified.
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Adds a new object to the storage.

        Parameters:
        obj: BaseModel instance - the object to be added
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file.
        """
        json_objects = {}
        for key, obj in self.__objects.items():
            json_objects[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key, value in jo.items():
                cls = classes[value["__class__"]]
                self.__objects[key] = cls(**value)
        except FileNotFoundError:
            # File does not exist, so no objects to load
            pass
        except json.JSONDecodeError:
            # File is not a valid JSON, handle accordingly
            pass

    def delete(self, obj=None):
        """
        Deletes an object from __objects if it exists.

        Parameters:
        obj: BaseModel instance - the object to be deleted
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            print('delete function not none', key)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls the reload() method to deserialize the JSON file to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves an object based on the class and its ID.

        Parameters:
        cls: class - the class of the object
        id: string - the ID of the object

        Returns:
        The object matching the class and ID, or None if not found.
        """
        if cls and id:
            key = "{}.{}".format(cls.__name__, id)
            return self.__objects.get(key, None)
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in storage matching the given class.

        Parameters:
        cls: class (optional) - if provided, counts objects of this class

        Returns:
        The number of objects in storage matching the class, or
        the total number if no class is specified.
        """
        if cls:
            cn = cls.__name__
            count = sum(1 for key in self.__objects if key.startswith(cn))
        else:
            count = len(self.__objects)
        return count
