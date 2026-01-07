from sqlalchemy import Column, UUID, Integer, DateTime, Index
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class MigrationModelFrameImage(Base):
    __tablename__ = "frame_images"
    id = Column[uuid.UUID](UUID(as_uuid=True), primary_key=True)
    camera_id = Column[int](Integer, nullable=False)
    view_id = Column[int](Integer, nullable=False)
    timestamp = Column[datetime](DateTime, nullable=False, index=True)
    __table_args__ = (
        Index(
            'index_timestamp_brin',
            'timestamp',
            postgresql_using='brin',
            postgresql_with={'pages_per_range': '64'}
        ),
        {"postgresql_partition_by": "RANGE (timestamp)"}
    )
