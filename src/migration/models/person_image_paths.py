from sqlalchemy import Column, Integer, DateTime, UUID, String
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class MigrationModelPersonImagePath(Base):
    __tablename__ = "person_image_paths"
    image_id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    timestamp = Column[datetime](DateTime)
    path = Column[str](String(255))
    created_at = Column[datetime](DateTime, default=datetime.now)
    updated_at = Column[datetime](
        DateTime, default=datetime.now, onupdate=datetime.now)
