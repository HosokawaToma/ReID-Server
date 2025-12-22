from sqlalchemy import Column, UUID, Integer, DateTime
from sqlalchemy.orm import declarative_base
import uuid
from pgvector.sqlalchemy import Vector
from datetime import datetime

Base = declarative_base()


class MigrationModelPersonSnapshot(Base):
    __tablename__ = "person_snapshots"
    id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    camera_id = Column[int](Integer, nullable=False)
    view_id = Column[int](Integer, nullable=False)
    timestamp = Column[datetime](DateTime, nullable=False)
    person_id = Column[uuid.UUID](UUID(as_uuid=True), nullable=True)
    feature = Column[Vector](Vector(1280), nullable=True)
