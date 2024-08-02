#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate our DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        # It creates the engine for the MySQL database connection
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        # Drop all tables if the environment is test
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        # Iterate over all classes
        for clss in classes:
            # If no class is specified or the class matches, query the objects
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                # Add each object to the new dictionary with its key
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        # Create all tables in the database
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Method that returns the object based on the class and its ID.

        Parameters:
        cls: class
        id: string representing the object ID

        Returns:
        The object based on the class and its ID, or None if not found
        """
        # Check if cls and id are provided
        if cls and id:
            # Ensure cls is a valid class
            if cls.__name__ in classes:
                # Query the object by ID
                return self.__session.query(classes[cls.__name__]).get(id)
        return None

    def count(self, cls=None):
        """
        Method that counts the number of object on the storage.

        Parameters:
        cls: class (optional)

        Returns:
        The number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage.
        """
        if cls:
            # Ensure cls is a valid class
            if cls.__name__ in classes:
                # Count the objects of the specified class
                return self.__session.query(classes[cls.__name__]).count()
        else:
            count = 0
            # Iterate over all classes and count their objects
            for clss in classes.values():
                count += self.__session.query(clss).count()
            return count
