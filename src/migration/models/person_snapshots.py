from sqlalchemy import UUID, Integer, DateTime, Boolean
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
import uuid
import torch
from pgvector.sqlalchemy import Vector
from datetime import datetime
import sqlalchemy as sa

Base = declarative_base()


class MigrationModelPersonSnapshot(Base):
    __tablename__ = "person_snapshots"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    camera_id: Mapped[int] = mapped_column(Integer, nullable=False)
    view_id: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_junk: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=sa.true())
    person_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, default=None, server_default=None)
    feature: Mapped[torch.Tensor | None] = mapped_column(Vector(1280), nullable=True, default=None, server_default=None)
