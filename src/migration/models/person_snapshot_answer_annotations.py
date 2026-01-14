from sqlalchemy import UUID, Boolean
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
import uuid

Base = declarative_base()

class MigrationModelPersonSnapshotAnswerAnnotation(Base):
    __tablename__ = "person_snapshot_answer_annotations"
    person_snapshot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, foreign_key="person_snapshots.id")
    person_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    is_junk: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
