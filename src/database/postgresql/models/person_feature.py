from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector
from datetime import datetime


Base = declarative_base()


class DatabasePostgreSQLModelPersonFeature(Base):
    __tablename__ = "person_features"
    feature = Column[Vector](Vector(1280))
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    timestamp = Column[datetime](DateTime)
