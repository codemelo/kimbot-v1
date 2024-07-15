from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class PositionDB(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    tg_msg_id = Column(String)
    tg_channel_id = Column(String)
    side = Column(String)
    symbol = Column(String)
    leverage = Column(Float)
    entry_low = Column(Float)
    entry_high = Column(Float)
    stop_loss = Column(Float)
    stopped = Column(Boolean)
    datetime = Column(DateTime)
    target_points = relationship("TargetPointDB", back_populates="position", order_by="TargetPointDB.target_number")


class TargetPointDB(Base):
    __tablename__ = 'target_points'

    position_id = Column(Integer, ForeignKey('positions.id'), primary_key=True)
    target_number = Column(Integer, primary_key=True)
    price = Column(Float)
    margin_percentage = Column(Float)

    position = relationship("PositionDB", back_populates="target_points")
