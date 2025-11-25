from sqlalchemy import Column, Integer, DateTime, UUID, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid
from pgvector.sqlalchemy import Vector

from migration.models.person_image_paths import MigrationModelPersonImagePath

Base = declarative_base()


class MigrationModelPersonFeature(Base):
    __tablename__ = "person_features"
    id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    image_id = Column[uuid.UUID](
        UUID(as_uuid=True), ForeignKey(MigrationModelPersonImagePath.image_id))
    person_id = Column[uuid.UUID](UUID(as_uuid=True))
    feature = Column[Vector](Vector(1280))
    camera_id = Column[int](Integer)
    view_id = Column[int](Integer)
    timestamp = Column[datetime](DateTime)
