from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Position, TargetPoint
from models_orm import Base, PositionORM, TargetPointORM
import config


engine = create_engine(config.DATABASE_URL) # Create the SQLite engine
Base.metadata.create_all(engine) # Create all tables in the engine
Session = sessionmaker(bind=engine) # Create a sessionmaker

class PositionRepository:
    def __init__(self):
        self.session = Session()

    def add(self, position: Position):
        position_orm = PositionORM(
            tg_msg_id=position.tg_msg_id,
            tg_channel_id=position.tg_channel_id,
            side=position.side,
            symbol=position.symbol,
            leverage=position.leverage,
            entry_low=position.entry_low,
            entry_high=position.entry_high,
            stop_loss=position.stop_loss,
            timestamp_utc=position.timestamp_utc
        )

        for tp in position.target_points:
            tp_orm = TargetPointORM(
                target_number=tp.target_number,
                price=tp.price,
                percentage=tp.percentage
            )
            position_orm.target_points.append(tp_orm)

        self.session.add(position_orm)
        self.session.commit()

    def get_all(self):
        position_orms = self.session.query(PositionORM).all()
        return [self._convert_to_domain(p) for p in position_orms]

    def _convert_to_domain(self, position_orm):
        position = Position(
            tg_msg_id=position_orm.tg_msg_id,
            tg_channel_id=position_orm.tg_channel_id,
            side=position_orm.side,
            symbol=position_orm.symbol,
            leverage=position_orm.leverage,
            entry_low=position_orm.entry_low,
            entry_high=position_orm.entry_high,
            stop_loss=position_orm.stop_loss,
            timestamp=position_orm.timestamp
        )

        for tp_orm in position_orm.target_points:
            position.add_target_point(tp_orm.price, tp_orm.percentage)

        return position

    def close(self):
        self.session.close()
