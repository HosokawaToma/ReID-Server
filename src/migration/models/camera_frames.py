"""
カメラフレームのマイグレーションモデル

camera_frames テーブルを定義する。
"""
from sqlalchemy import UUID, Integer, DateTime, Index
from sqlalchemy.orm import mapped_column, Mapped
import uuid
from datetime import datetime
from .base import Base


class MigrationModelCameraFrame(Base):
    """
    カメラフレームを保存するテーブル。

    id, camera_id, view_id, timestamp を保持する。
    """
    __tablename__ = "camera_frames"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    camera_id: Mapped[int] = mapped_column(Integer, nullable=False)
    view_id: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        Index(
            'index_timestamp',
            'timestamp',
        ),
        Index(
            'index_camera_id_view_id_timestamp',
            'camera_id',
            'view_id',
            'timestamp',
        ),
    )
