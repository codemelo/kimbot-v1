from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from .db_models import PositionDB, TargetPointDB
from src.models import Position, TargetPoint
from utils import config


class DataManager:
    def __init__(self, db_url=config.DATABASE_URL):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_position(self, tg_msg_id, tg_channel_id, side, symbol, leverage, entry_low, entry_high, stop_loss, datetime):
        session = self.Session()
        new_position_db = PositionDB(
            tg_msg_id=tg_msg_id,
            tg_channel_id=tg_channel_id,
            side=side,
            symbol=symbol,
            leverage=leverage,
            entry_low=entry_low,
            entry_high=entry_high,
            stop_loss=stop_loss,
            stopped=False,
            datetime=datetime
        )
        session.add(new_position_db)
        session.commit()
        new_position = self._map_db_to_position(new_position_db)
        session.close()
        return new_position

    def _map_db_to_position(self, position_db):
        position = Position(
            position_id=position_db.id,
            tg_msg_id=position_db.tg_msg_id,
            tg_channel_id=position_db.tg_channel_id,
            side=position_db.side,
            symbol=position_db.symbol,
            leverage=position_db.leverage,
            entry_low=position_db.entry_low,
            entry_high=position_db.entry_high,
            stop_loss=position_db.stop_loss,
            stopped=position_db.stopped,
            datetime=position_db.datetime
        )
        for tp_db in position_db.target_points:
            tp = TargetPoint(
                price=tp_db.price,
                percentage=tp_db.margin_percentage,
                target_number=tp_db.target_number
            )
            position.target_points.append(tp)
        return position

    def _map_position_to_db(self, position, position_db=None):
        if position_db is None:
            position_db = PositionDB()

        position_db.tg_msg_id = position.tg_msg_id
        position_db.tg_channel_id = position.tg_channel_id
        position_db.side = position.side
        position_db.symbol = position.symbol
        position_db.leverage = position.leverage
        position_db.entry_low = position.entry_low
        position_db.entry_high = position.entry_high
        position_db.stop_loss = position.stop_loss
        position_db.stopped = position.stopped
        position_db.datetime = position.datetime

        for tp in position.target_points:
            tp_db = TargetPointDB(
                price=tp.price,
                margin_percentage=tp.margin_percentage,
                target_number=tp.target_number,
                reached=tp.reached,
                datetime=tp.datetime,
                profit_percentage=tp.profit_percentage
            )
            position_db.target_points.append(tp_db)

        return position_db

    def save_position(self, position):
        session = self.Session()
        position_db = self._map_position_to_db(position)
        session.add(position_db)
        session.commit()
        session.close()
