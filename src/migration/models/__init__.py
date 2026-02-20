"""
マイグレーション用 ORM モデル

SQLAlchemy モデルと Alembic 用メタデータをエクスポートする。
"""
from .base import Base
from .person_snapshots import MigrationModelPersonSnapshot
from .camera_frames import MigrationModelCameraFrame
from .person_snapshots_answer_labels import MigrationModelPersonSnapshotsAnswerLabels

ALEMBIC_MODELS = Base.metadata
