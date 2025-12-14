from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class MigrationModelFrameImage(Base):
    __tablename__ = "frame_images"
    id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    timestamp = Column[datetime](DateTime)
