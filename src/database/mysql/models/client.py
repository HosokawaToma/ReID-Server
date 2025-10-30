from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base()

class DatabaseMySQLModelClient(Base):
    __tablename__ = "clients"
    id = Column[str](String(255), primary_key=True)
    hashed_password = Column[str](String(255))
    created_at = Column[datetime](DateTime, default=datetime.now)
    updated_at = Column[datetime](DateTime, default=datetime.now)
