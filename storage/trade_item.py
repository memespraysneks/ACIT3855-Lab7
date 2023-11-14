from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class TradeItem(Base):
    """ Trade Item """

    __tablename__ = "trade_item"

    id = Column(Integer, primary_key=True)
    trade_id = Column(String(250), nullable=False)
    initial_user_id = Column(String(250), nullable=False)
    secondary_user_id = Column(String(250), nullable=False)
    offer_item_id = Column(String(250), nullable=False)
    offer_item_strength = Column(Integer, nullable=False)
    offer_item_dexterity = Column(Integer, nullable=False)
    offer_item_intelligence = Column(Integer, nullable=False)
    trade_item_id = Column(String(250), nullable=False)
    trade_item_strength = Column(Integer, nullable=False)
    trade_item_dexterity = Column(Integer, nullable=False)
    trade_item_intelligence = Column(Integer, nullable=False)
    timestamp = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(250), nullable=False)

    def __init__(self, trade_id, initial_user_id, secondary_user_id, offer_item_id, offer_item_strength, offer_item_dexterity, offer_item_intelligence, trade_item_id, trade_item_strength, trade_item_dexterity, trade_item_intelligence, timestamp, trace_id):
        """ Initializes a trade """
        self.trade_id = trade_id
        self.initial_user_id = initial_user_id
        self.secondary_user_id = secondary_user_id
        self.offer_item_id = offer_item_id
        self.offer_item_strength = offer_item_strength
        self.offer_item_dexterity = offer_item_dexterity
        self.offer_item_intelligence = offer_item_intelligence
        self.trade_item_id = trade_item_id
        self.trade_item_strength = trade_item_strength
        self.trade_item_dexterity = trade_item_dexterity
        self.trade_item_intelligence = trade_item_intelligence
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.trace_id = trace_id

    def to_dict(self):
        """ Dictionary Representation of a trade """
        dict = {}
        dict['id'] = self.id
        dict['trade_id'] = self.trade_id
        dict['initial_user_id'] = self.initial_user_id
        dict['secondary_user_id'] = self.secondary_user_id
        dict['offer_item'] = {}
        dict['offer_item']['item_id'] = self.offer_item_id
        dict['offer_item']['strength'] = self.offer_item_strength
        dict['offer_item']['dexterity'] = self.offer_item_dexterity
        dict['offer_item']['intelligence'] = self.offer_item_intelligence
        dict['trade_item'] = {}
        dict['trade_item']['item_id'] = self.trade_item_id
        dict['trade_item']['strength'] = self.trade_item_strength
        dict['trade_item']['dexterity'] = self.trade_item_dexterity
        dict['trade_item']['intelligence'] = self.trade_item_intelligence
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created
        dict['trace_id'] = self.trace_id

        return dict
