from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

class Rooms(BASE):
    """This is the class architecture for creating the Room table using SQLAlchemy."""
    def __init__(self, room_name, room_type, current_occupants, num_of_occupants, max_capacity,):
        self.room_name = room_name
        self.current_occupants = current_occupants
        self.num_of_occupants = num_of_occupants
        self.max_capacity = max_capacity
        self.room_type = room_type
    #Creating my table columns and assigning a Table name
    __tablename__ = 'Rooms'
    room_name = Column(String, primary_key=True)
    room_type = Column(String)
    num_of_occupants = Column(Integer)
    current_occupants = Column(String)
    max_capacity = Column(Integer)

class Person(BASE):
    """"This is the class architecture for creating the Person table using SQLAlchemy."""
    def __init__(self, id_number, name, allocation_status, person_type):
        self.id_number = id_number
        self.name = name
        self.allocation_status = allocation_status
        self.person_type = person_type
    #Creating my table columns and assigning a table name
    __tablename__ = 'People'
    id_number = Column(Integer, primary_key=True)
    name = Column(String)
    allocation_status = Column(Boolean)
    person_type = Column(String)


def create_db(filename='amity'):
    """This function creates database tables in sqlite according to the templates given above."""
    engine = create_engine('sqlite:///'+filename+'.db')
    return BASE.metadata.create_all(engine)



                