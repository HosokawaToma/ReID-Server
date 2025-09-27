from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Clients(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True)
    hashed_password = Column(String)

    def __repr__(self):
        return "<Clients(id={}, hashed_password={})>".format(self.id, self.hashed_password)
