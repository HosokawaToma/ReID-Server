from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class DatabaseMySQLModelClientCamera(Base):
    __tablename__ = "clients_camera"
    client_id = Column[str](String(255), ForeignKey("clients.id"), primary_key=True)
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    created_at = Column[datetime](DateTime, default=datetime.now)
    updated_at = Column[datetime](DateTime, default=datetime.now)
