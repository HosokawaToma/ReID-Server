from .base import Base
from .person_snapshots import MigrationModelPersonSnapshot
from .camera_frames import MigrationModelCameraFrame
from .person_snapshots_answer_labels import MigrationModelPersonSnapshotsAnswerLabels

# すべてのモデルが同じBaseを使用するため、単一のメタデータオブジェクトを使用
ALEMBIC_MODELS = Base.metadata
