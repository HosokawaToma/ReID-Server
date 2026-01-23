from sqlalchemy import UUID, Integer, Float, Index, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
import uuid

Base = declarative_base()


class MigrationModelPersonSnapshotDetection(Base):
    __tablename__ = "person_snapshot_detections"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    person_snapshot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("person_snapshots.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    x: Mapped[int] = mapped_column(Integer, nullable=False)
    y: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        Index('index_person_snapshot_id', 'person_snapshot_id'),
    )
