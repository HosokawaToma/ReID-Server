from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cameras(Base):
    __tablename__ = "cameras"

    client_id = Column(String, ForeignKey("clients.id"), primary_key=True)
    camera_id = Column(Integer)
    view_id = Column(Integer)

    def __repr__(self):
        return "<Clients(client_id={}, camera_id={}, view_id={})>".format(self.client_id, self.camera_id, self.view_id)
