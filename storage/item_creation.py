from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class CreateItem(Base):
    """ Create Item """

    __tablename__ = "item_creation"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), nullable=False)
    item_id = Column(String(250), nullable=False)
    strength = Column(Integer, nullable=False)
    dexterity = Column(Integer, nullable=False)
    intelligence = Column(Integer, nullable=False)
    timestamp = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)
    

    def __init__(self, user_id, item_id, strength, dexterity, intelligence, timestamp, trace_id):
        """ Initializes a blood pressure reading """
        self.user_id = user_id
        self.item_id = item_id
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a item creation """
        dict = {}
        dict['id'] = self.id
        dict['user_id'] = self.user_id
        dict['item'] = {}
        dict['item']['item_id'] = self.item_id
        dict['item']['strength'] = self.strength
        dict['item']['dexterity'] = self.dexterity
        dict['item']['intelligence'] = self.intelligence
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
