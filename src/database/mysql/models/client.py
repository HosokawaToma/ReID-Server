from sqlalchemy import Column, String, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DatabaseMySQLModelClient(Base):
    __tablename__ = "clients"
    id = Column[str](String(255), primary_key=True)
    hashed_password = Column[str](String(255))
    created_at = Column[datetime](DateTime, default=datetime.now())
    updated_at = Column[datetime](DateTime, default=datetime.now(), onupdate=datetime.now())
