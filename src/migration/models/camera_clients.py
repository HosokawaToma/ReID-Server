from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class MigrationModelCameraClient(Base):
    __tablename__ = "camera_clients"
    id = Column[str](String(255), primary_key=True)
    hashed_password = Column[str](String(255))
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    created_at = Column[datetime](DateTime, default=datetime.now)
    updated_at = Column[datetime](
        DateTime, default=datetime.now, onupdate=datetime.now)
