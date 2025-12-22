from sqlalchemy import Column, UUID, Integer, DateTime, Boolean
from sqlalchemy.orm import declarative_base
import uuid
from pgvector.sqlalchemy import Vector
from datetime import datetime
import sqlalchemy as sa

Base = declarative_base()


class MigrationModelPersonSnapshot(Base):
    __tablename__ = "person_snapshots"
    id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    camera_id = Column[int](Integer, nullable=False)
    view_id = Column[int](Integer, nullable=False)
    timestamp = Column[datetime](DateTime, nullable=False)
    is_junk = Column[bool](Boolean, nullable=False, default=True, server_default=sa.true())
    person_id = Column[uuid.UUID](UUID(as_uuid=True), nullable=True, default=None, server_default=None)
    feature = Column[Vector](Vector(1280), nullable=True, default=None, server_default=None)
