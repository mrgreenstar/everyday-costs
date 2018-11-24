from datetime import date

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError

Base = declarative_base()

class Costs(Base):
    __tablename__ = "everydayCosts"
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=date.today())
    bought_thing = Column(String(100))
    amount = Column(Float)
    comment = Column(String(100), default="No comment")

    def __init__(self, bought_thing, amount, comment=None):
        self.bought_thing = bought_thing
        self.amount = amount
        self.comment = comment
    
    def __repr__(self):
        return "<Costs (id: {}, date: {}, bought_thing: {}, amount: {}, comment: {})>".format(
            self.id, self.date, self.bought_thing, self.amount, self.comment
        )

class SingleSession():
    _instance = None

    @staticmethod
    def getInstance():        
        if SingleSession._instance == None:
            try:
                engine = create_engine("mysql://mrgreenstar:ThePassword@localhost:3306/everyday_costs")
                Base.metadata.create_all(engine)
                Session = sessionmaker(bind=engine)
                SingleSession()
                SingleSession._instance = Session()
            except OperationalError:
                print("Can't connect to database")
        return SingleSession._instance
