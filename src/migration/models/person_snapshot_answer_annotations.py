from sqlalchemy import UUID, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
import uuid

Base = declarative_base()

class MigrationModelPersonSnapshotAnswerAnnotation(Base):
    __tablename__ = "person_snapshot_answer_annotations"
    person_snapshot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("person_snapshots.id"), primary_key=True)
    person_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    is_junk: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
