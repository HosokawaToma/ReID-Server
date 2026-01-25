from .person_snapshots import MigrationModelPersonSnapshot
from .camera_frames import MigrationModelCameraFrame
from .person_snapshots_answer_labels import MigrationModelPersonSnapshotsAnswerLabels

ALEMBIC_MODELS = [
    MigrationModelPersonSnapshot.metadata,
    MigrationModelCameraFrame.metadata,
    MigrationModelPersonSnapshotsAnswerLabels.metadata,
]
