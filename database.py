from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///HOTSIX.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'userdata'
    id = Column(Integer, primary_key = True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Animal(Base):
    __tablename__ = 'animaldata'
    id = Column(Integer, primary_key = True)
    owner = Column(String)
    animal_name = Column(String)
    animal_age = Column(Integer)
    animal_register_date = Column(Integer)
    animal_weight = Column(Integer)
    animal_kind = Column(String)
    animal_sex = Column(String)

    def __init__(self, owner, animal_name, animal_age, animal_register_date, animal_weight, animal_kind, animal_sex):
        self.owner = owner
        self.animal_name = animal_name
        self.animal_age = animal_age
        self.animal_register_date = animal_register_date
        self.animal_weight = animal_weight
        self.animal_kind = animal_kind
        self.animal_sex = animal_sex

Base.metadata.create_all(engine)
