from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class TargetPoint(Base):
    __tablename__ = 'target_points'

    position_id = Column(Integer, ForeignKey('positions.id'), primary_key=True)
    target_number = Column(Integer, primary_key=True)
    price = Column(Float)
    margin_percentage = Column(Float)
    reached = Column(Boolean)
    datetime = Column(DateTime)
    profit_percentage = Column(Float)

    position = relationship("Position", back_populates="target_points")

    def __init__(self, price: float, percentage: float):
        self.position = None
        self.target_number = None
        self.price = price
        self.margin_percentage = percentage
        self.profit_percentage = None
        self.reached = False
        self.datetime = None
