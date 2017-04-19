from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#Association Table
# occupants = Table('occupants', Base.metadata,
#                     Column('name', ForeignKey('rooms.name'),primary_key=True),
#                     Column('id', Integer, ForeignKey('People.id'),primary_key=True)
#                         )
class Room(Base):
    def __init__(self, room_name, current_occupants, max_capacity):
        self.room_name = room_name 
        self.current_occupants = current_occupants
        self.max_capacity = max_capacity

    __tablename__ = 'rooms'
    room_name = Column(String,primary_key=True)
    current_occupants = Column(String)
    max_capacity = Column(Integer)

class Person(Base):
    def __init__(self, id_number, name, allocation_status):
        self.id_number = id_number
        self.name = name
        self.allocation_status = allocation_status  
    
    __tablename__ = 'people'
    id_number = Column(Integer, primary_key=True)
    name = Column(String)
    allocation_status = Column(Boolean)


def create_db(filename='amity'):
    engine = create_engine('sqlite:///'+filename+'.db')
    return Base.metadata.create_all(engine)
# class Room(Base):

#     __tablename__ = 'rooms'
#     name = Column(String, primary_key = True)
#     num_of_persons = Column(Integer)
#     current_occupants = relationship('People', 
#                                     secondary= occupants,
#                                     backref='rooms',
#                                     order_by= 'name')
    
    # def __repr__(self):
    #     return "<Room(name='%s', num_of_persons='%s', current_occupants='%s')>" % (
    #                          self.name, self.num_of_persons, self.current_occupants)

# class People(Base):

    
#     __tablename__ = 'People'
#     name = Column(String)
#     id = Column(String, primary_key = True)
#     is_allocated = Column(Boolean, nullable=False)
    

    # def __repr__(self):
    #     return "<Person(name='%s', employee_id='%s', is_allocated='%s')>" % (
    #                          self.name, self.employee_id, self.is_allocated)


# class SqlDatabase:

#     def __init__(self, filename):
    
#         self.engine = create_engine('sqlite:///'+filename)
#         self.Session = sessionmaker()
#         self.Session.configure(bind=self.engine)
#         self.session = self.Session()
#         Base.metadata.create_all(self.engine)
    
    
#     def refresh(self):
#         self.__init__(SqlDatabase)
    
#     def close(self):
#         import pdb; pdb.set_trace()
#         self.session.commit()
#         self.session.close()
    


                