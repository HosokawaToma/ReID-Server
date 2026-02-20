"""
マイグレーション用 ORM モデル

SQLAlchemy モデルと Alembic 用メタデータをエクスポートする。
"""
from .base import Base
from .person_snapshots import MigrationModelPersonSnapshot
from .camera_frames import MigrationModelCameraFrame
from .person_snapshots_answer_labels import MigrationModelPersonSnapshotsAnswerLabels

# すべてのモデルが同じ Base を使用するため、単一のメタデータオブジェクトを使用
ALEMBIC_MODELS = Base.metadata
