from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.position import Position
from src.models.base import Base
from utils import config


class DataManager:
    def __init__(self, db_url=config.DATABASE_URL):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_position(self):
        session = self.Session()
        new_position = Position()
        session.add(new_position)
        session.commit()
        session.close()
        return new_position

    def add_target_point(self, position_id):
        session = self.Session()
        position = session.query(Position).get(position_id)
        if position:
            new_target = position.add_target_point()
            session.add(new_target)
            session.commit()
        session.close()
        return new_target

    # Add more methods for querying, updating, deleting, etc.
