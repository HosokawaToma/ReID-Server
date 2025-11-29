from sqlalchemy import Column, Integer, DateTime, UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class MigrationModelPersonSnapshot(Base):
    __tablename__ = "person_snapshots"
    id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    image_id = Column[uuid.UUID](UUID(as_uuid=True))
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    timestamp = Column[datetime](DateTime)
    person_id = Column[uuid.UUID](UUID(as_uuid=True))
    feature = Column[Vector](Vector(1280), nullable=True)
