#!/usr/bin/python3
""" DBStorage Module """

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {'State': State, 'City': City, 'User': User,
           'Place': Place, 'Review': Review, 'Amenity': Amenity}


class DBStorage:
    """ Database storage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialization of DBStorage """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query all objects of a certain class """
        new_dict = {}
        if cls is None:
            for key, value in classes.items():
                for obj in self.__session.query(value).all():
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        else:
            for obj in self.__session.query(cls).all():
                key = obj.__class__.__name__ + "." + obj.id
                new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete obj from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ reload method """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Close the current session """
        self.__session.close()
