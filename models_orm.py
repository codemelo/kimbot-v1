from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import config

Base = declarative_base()

class PositionORM(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    tg_msg_id = Column(String)
    tg_channel_id = Column(String)
    side = Column(String)
    symbol = Column(String)
    leverage = Column(Float)
    entry_low = Column(Float)
    entry_high = Column(Float)
    stop_loss = Column(Float)
    timestamp_utc = Column(DateTime)

    target_points = relationship("TargetPointORM", back_populates="position", cascade="all, delete-orphan")

class TargetPointORM(Base):
    __tablename__ = 'target_points'

    id = Column(Integer, primary_key=True)
    target_number = Column(Integer)
    price = Column(Float)
    percentage = Column(Float)
    position_id = Column(Integer, ForeignKey('positions.id'))

    position = relationship("PositionORM", back_populates="target_points")
