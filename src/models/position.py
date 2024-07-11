from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    side = Column(String)
    symbol = Column(String)
    leverage = Column(Float)
    entry_low = Column(Float)
    entry_high = Column(Float)
    stop_loss = Column(Float)
    stopped = Column(Boolean)
    datetime = Column(DateTime)
    target_points = relationship("TargetPoint", back_populates="position", order_by="TargetPoint.target_number")

    def __init__(self):
        self.side = None
        self.symbol = None
        self.leverage = None
        self.entry_low = None
        self.entry_high = None
        self.stop_loss = None
        self.stopped = None
        self.datetime = None
        self.target_points = []

    def add_target_point(self, price: float, percentage: float):
        from .target_point import TargetPoint
        target_number = len(self.target_points) + 1
        tp = TargetPoint(price, percentage)
        tp.target_number = target_number
        self.target_points.append(tp)
