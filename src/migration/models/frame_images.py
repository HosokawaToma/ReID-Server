from sqlalchemy import Column, UUID, Integer, DateTime
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class MigrationModelFrameImage(Base):
    __tablename__ = "frame_images"
    id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    camera_id = Column[int](Integer, nullable=False)
    view_id = Column[int](Integer, nullable=False)
    timestamp = Column[datetime](DateTime, nullable=False)
