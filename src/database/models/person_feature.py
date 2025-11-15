from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class DatabaseModelPersonFeature(Base):
    __tablename__ = "person_features"
    id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    person_id = Column[uuid.UUID](UUID(as_uuid=True))
    feature = Column[Vector](Vector(1280))
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    timestamp = Column[datetime](DateTime)
